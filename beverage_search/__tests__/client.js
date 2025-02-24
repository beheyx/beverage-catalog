const zmq = require("zeromq");
const readline = require('node:readline');

const getQuestionByOption = (option) => {
  switch (option) {
    case '1':
      return 'Enter the recipe name you are looking for: ';
    case '2':
      return 'Enter the type of beverages you are looking for: ';
    case '3':
      return 'Enter an ingredient you are looking for in beverages: ';
    default:
      throw new Error(`Unknown option: ${option}`);
  }
}

const askQuestion = (rl, question) => {
  return new Promise((resolve) => rl.question(question, resolve));
};

async function run() {
  const sock = new zmq.Request();

  sock.connect(`tcp://localhost:5553`);

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  while (true) {
    console.log("\nWhat would you like to do?");
    console.log("1) Search Recipe by Name");
    console.log("2) Filter Beverages by Type");
    console.log("3) Filter Beverages by Ingredient");

    const option = await askQuestion(rl, '\nEnter a choice from 1 to 3: ');
    const question = getQuestionByOption(option);
    const userInput = await askQuestion(rl, question);

    await sock.send(`${option}:${userInput}`);

    const [response] = await sock.receive();

    if (response.toString() === 'not found') {
      console.log('No recipe found.');
    } else {
      console.log(response.toString());
    }
  }
}

run();