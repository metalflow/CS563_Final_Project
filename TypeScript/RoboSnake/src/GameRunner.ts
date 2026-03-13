import { initializeAgent, Motion, agentMove } from "./Agent";
import { scheduleNextUpdate, updateApples, updateLost } from "./DrawingLibrary";
import { Cell, draw, GameScreen } from "./GameScreen";

// a MaybeCell is either a Cell or the string "outside"
export type MaybeCell = Cell | "outside";

// a ScreenPart is a 5x5 array of MaybeCell arrays
export type ScreenPart = MaybeCell[][];

export class Point {
  public x: number;
  public y: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}

export class SnakeState extends Point {
  public apples: number;
  public lost: boolean;

  constructor(x: number, y: number) {
    super(x, y); // call Point constructor to set x and y
    this.apples = 0;
    this.lost = false;
  }

  public setPoint(p: Point): void {
    this.x = p.x;
    this.y = p.y;
  }
}

// x and y are the left and top coordinate of a 5x5 square region.
// cells outside the bounds of the board are represented with "outside"
export function getScreenPart(screen: GameScreen, s: SnakeState): ScreenPart {
  const part: ScreenPart = new Array<MaybeCell[]>(5);
  for (let j = 0; j < 5; j++) {
    part[j] = new Array<MaybeCell>(5);
    for (let i = 0; i < 5; i++) {
      if (s.x+i-2 >= 0 && s.y-2 + j >= 0 && s.x-2 + i < screen.length && s.y-2 + j < screen.length)
        part[j][i] = screen[s.y+j-2][s.x+i-2];
      else
        part[j][i] = "outside";
    }
  }
  return part;
}

// stepTime is a number of milliseconds
export function run(stepTime: number, newApplesEachStep: number, screen: GameScreen): void {
  initializeAgent("A");
  initializeAgent("B");
  initializeAgent("C");
  initializeAgent("D");

  // player initial positions
  const a = new SnakeState(0,0);
  const b = new SnakeState(screen.length - 1, 0);
  const c = new SnakeState(0, screen.length - 1);
  const d = new SnakeState(screen.length - 1, screen.length - 1);

  // draw starting screen
  screen[a.y][a.x] = "A";
  screen[b.y][b.x] = "B";
  screen[c.y][c.x] = "C";
  screen[d.y][d.x] = "D";
  draw(screen);

  // this will wait for stepTime milliseconds and then call step with these arguments
  scheduleNextUpdate(stepTime, () => step(stepTime, newApplesEachStep, screen, a, b, c, d));
  // the "() =>" part is important!
  // without it, step will get called immediately instead of waiting
}

function locationAfterMotion(motion: Motion, snake: SnakeState): Point {
  switch (motion) {
    case "left": return new Point(snake.x-1, snake.y);
    case "right": return new Point(snake.x+1, snake.y);
    case "up": return new Point(snake.x, snake.y-1);
    case "down": return new Point(snake.x, snake.y+1);
  }
}

export function step(
  stepTime: number,
  newApplesEachStep: number,
  screen: GameScreen,
  snakeA: SnakeState,
  snakeB: SnakeState,
  snakeC: SnakeState,
  snakeD: SnakeState
): void {
  // generate new apples
  for (let i = 0; i < newApplesEachStep; i++) {
    // random integers in the closed range [0, screen.length]
    const x = Math.floor(Math.random() * screen.length);
    const y = Math.floor(Math.random() * screen.length);
    // if we generated coordinates that aren't empty, skip this apple
    if (screen[y][x] == "empty")
      screen[y][x] = "apple";
  }

  // players take turns in order: A -> B -> C -> D -> A -> B -> C -> D -> ...

  if (!snakeA.lost) {
    const temp = locationAfterMotion(agentMove("A", getScreenPart(screen, snakeA)), snakeA);
    if (temp.x < 0 || temp.y < 0 || temp.x >= screen.length || temp.y >= screen.length) // hit the edge of the screen
      snakeA.lost = true;
    else
      switch (screen[temp.y][temp.x]) {
        case "empty": { // make the move
          snakeA.setPoint(temp);
          screen[temp.y][temp.x] = "A";
          break;
        }
        case "apple": { // make the move and eat the apple
          snakeA.setPoint(temp);
          snakeA.apples++;
          screen[temp.y][temp.x] = "A";
          break;
        }
        default: { // lose
          snakeA.lost = true;
          break;
        }
      }
  }

  if (!snakeB.lost) {
    const temp = locationAfterMotion(agentMove("B", getScreenPart(screen, snakeB)), snakeB);
    if (temp.x < 0 || temp.y < 0 || temp.x >= screen.length || temp.y >= screen.length) // hit the edge of the screen
      snakeB.lost = true;
    else
      switch (screen[temp.y][temp.x]) {
        case "empty": { // make the move
          snakeB.setPoint(temp);
          screen[temp.y][temp.x] = "B";
          break;
        }
        case "apple": { // make the move and eat the apple
          snakeB.setPoint(temp);
          snakeB.apples++;
          screen[temp.y][temp.x] = "B";
          break;
        }
        default: { // lose
          snakeB.lost = true;
          break;
        }
      }
  }

  if (!snakeC.lost) {
    const temp = locationAfterMotion(agentMove("C", getScreenPart(screen, snakeC)), snakeC);
    if (temp.x < 0 || temp.y < 0 || temp.x >= screen.length || temp.y >= screen.length) // hit the edge of the screen
      snakeC.lost = true;
    else
      switch (screen[temp.y][temp.x]) {
        case "empty": { // make the move
          snakeC.setPoint(temp);
          screen[temp.y][temp.x] = "C";
          break;
        }
        case "apple": { // make the move and eat the apple
          snakeC.setPoint(temp);
          snakeC.apples++;
          screen[temp.y][temp.x] = "C";
          break;
        }
        default: { // lose
          snakeC.lost = true;
          break;
        }
      }
  }

  if (!snakeD.lost) {
    const temp = locationAfterMotion(agentMove("D", getScreenPart(screen, snakeD)), snakeD);
    if (temp.x < 0 || temp.y < 0 || temp.x >= screen.length || temp.y >= screen.length) // hit the edge of the screen
      snakeD.lost = true;
    else
      switch (screen[temp.y][temp.x]) {
        case "empty": { // make the move
          snakeD.setPoint(temp);
          screen[temp.y][temp.x] = "D";
          break;
        }
        case "apple": { // make the move and eat the apple
          snakeD.setPoint(temp);
          snakeD.apples++;
          screen[temp.y][temp.x] = "D";
          break;
        }
        default: { // lose
          snakeD.lost = true;
          break;
        }
      }
  }


  // update game screen
  draw(screen);

  // update snake statistics
  updateLost("A", snakeA.lost); updateApples("A", snakeA.apples);
  updateLost("B", snakeB.lost); updateApples("B", snakeB.apples);
  updateLost("C", snakeC.lost); updateApples("C", snakeC.apples);
  updateLost("D", snakeD.lost); updateApples("D", snakeD.apples);

  // run again unless everyone has lost
  if (!snakeA.lost || !snakeB.lost || !snakeC.lost || !snakeD.lost)
    scheduleNextUpdate(stepTime, () => step(stepTime, newApplesEachStep, screen, snakeA, snakeB, snakeC, snakeD));
}