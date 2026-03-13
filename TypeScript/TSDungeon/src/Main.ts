// A Room value is exactly one of these four strings.
// It is impossible for a Room variable to contain any other string.
type Room = "A" | "B" | "C" | "Exit";

export function play(): void {
  console.info("Welcome to the text adventure! Open your browser's developer console to play.");

  console.warn("Please enter your name.");
  let playerName: string | null = prompt("Please enter your name.");
  while (playerName == null || playerName == "") {
    console.error("Invalid input.");
    playerName = prompt("Please enter your name.");
  }
  console.log(playerName);

  console.info("Hello, " + playerName + ".");

  console.info("You are in a building. Your goal is to exit this building.");
  console.info("You are in an empty room. There are doors on the north and west walls of this room.");

  let currentRoom: Room = "A";
  let hasKey: boolean = false;
  let windowOpen: boolean = false;

  while (currentRoom != "Exit") {
    console.warn("Please enter a command.");
    let command: string | null = prompt("Please enter a command.");
    while (command == null || command == "") {
      console.error("Invalid input.");
      command = prompt("Please enter a command.");
    }
    console.log(command);

    switch (currentRoom) {
      case "A":
        switch (command) {
          case "west":
            currentRoom = "B";
            console.info("You go through the west door. You are in a room with a table.");
            if (!hasKey) {
              console.info("On the table there is a key.");
            }
            console.info("There is a door on the east wall of this room.");
            break;
          case "north":
            if (hasKey) {
              currentRoom = "C";
              console.info("You unlock the north door with the key and go through the door.");
              console.info("You are in a bright room. There is a door on the south wall of this room and a window on the east wall.");
            } else {
              console.error("You try to open the north door, but it is locked.");
            }
            break;
          default:
            console.error("Unrecognized command.");
            break;
        }
        break;

      case "B":
        switch (command) {
          case "east":
            currentRoom = "A";
            console.info("You are in an empty room. There are doors on the north and west walls of this room.");
            break;
          case "take key":
            if (hasKey) {
              console.error("You already have the key.");
            } else {
              console.info("You take the key from the table.");
              hasKey = true;
            }
            break;
          default:
            console.error("Unrecognized command.");
            break;
        }
        break;

      case "C":
        switch (command) {
          case "south":
            currentRoom = "A";
            console.info("You are in an empty room. There are doors on the north and west walls of this room.");
            break;
          case "east":
            if (windowOpen) {
              currentRoom = "Exit";
              console.info("You step out from the open window.");
            } else {
              console.error("The window is closed.");
            }
            break;
          case "open window":
            if (windowOpen) {
              console.error("The window is already open.");
            } else {
              console.info("You open the window.");
              windowOpen = true;
            }
            break;
          default:
            console.error("Unrecognized command.");
            break;
        }
        break;
    }
  }

  console.info("You have exited the building. You win!");
  console.info("Congratulations, " + playerName + "!");
}
