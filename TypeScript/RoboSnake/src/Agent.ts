import { MaybeCell, ScreenPart } from "./GameRunner";

export type Player = "A" | "B" | "C" | "D";

export type Motion = "up" | "down" | "left" | "right";

// C uses these moves in order, repeatedly
const cCycle: Motion[] = ["up", "up", "right", "down", "right"];
let cIndex: number = 0;

export function initializeAgent(player: Player): void {
  // only agent C has its own state (for now)
  if (player == "C") cIndex = 0;
}

// screenPart is a 5x5 window with the agent in the center
export function agentMove(player: Player, screenPart: ScreenPart): Motion {
  switch (player) {
    case "A": { // always move right
      return "right";
    }
    case "B": { // always random
      return randomMotion(screenPart);
    }

    case "C": { // cycle through the moves in cCycle
      const c: Motion = cCycle[cIndex];
      cIndex++;
      cIndex = cIndex % cCycle.length;
      return c;
    }

    case "D": { // go for any nearby apple, otherwise random
      for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
          if (screenPart[j][i] == "apple") {
            if (i > 3) return "right";
            else if (i < 3) return "left";
            else if (j > 3) return "down";
            else if (j < 3) return "up";
          }
        }
      }
      return randomMotion(screenPart);
    }
  }
}

export function randomMotion(part: ScreenPart): Motion {
  const rnd: number = Math.random() * 4; // random float in the half-open range [0, 4)

  let x: Motion;
  if (rnd < 1) x = "up";
  else if (rnd < 2) x = "down";
  else if (rnd < 3) x = "left";
  else x = "right";

  // try not to hit anything
  if (tryMove(x, part) != "apple" && tryMove(x, part) != "empty") {
    switch (x) {
      case "up": return "down";
      case "right": return "left";
      case "down": return "up";
      case "left": return "right";
    }
  }

  return x;
}

function tryMove(m: Motion, p: ScreenPart): MaybeCell {
  // the snake is positioned in the center at p[2][2]
  switch (m) {
    case "left": return p[2][1];
    case "right": return p[2][3];
    case "up": return p[1][2];
    case "down": return p[3][2];
  }
}