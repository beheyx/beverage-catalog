const fs = require('fs').promises;

const loadBeverages = async () => {
  try {
    const data = await fs.readFile(process.env.JSON_PATH, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.log(error);
  }
}

module.exports = { loadBeverages };