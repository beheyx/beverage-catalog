const zmq = require("zeromq");

require('dotenv').config();

const { searchByName, filterByCategory, filterByIngredients } = require("./services/utils");
const { loadBeverages } = require("./services/storage");

const commandMap = {
  1: searchByName,
  2: filterByCategory,
  3: filterByIngredients,
};

async function run() {
  const sock = new zmq.Reply();

  await sock.bind(`tcp://localhost:${process.env.TCP_PORT}`);

  const beverages = await loadBeverages();

  for await (const [msg] of sock) {
    const [cmd, userInput] = msg.toString().split(':');

    if (!commandMap[cmd]) {
      return 'wrong command';
    }

    const result = commandMap[cmd](userInput.trim(), beverages);

    await sock.send(result);
  }
}

run();
