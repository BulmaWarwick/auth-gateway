const { parse } = require('node-html-parser');
const chalk = require('chalk');

class LoginParser {
  constructor(html) {
    this.html = html;
  }

  parse() {
    const root = parse(this.html);
    const form = root.querySelector('form');
    const inputs = form.querySelectorAll('input');

    this.usernameInput = inputs.find((input) => input.getAttribute('name') === 'username');
    this.passwordInput = inputs.find((input) => input.getAttribute('name') === 'password');
  }

  get username() {
    return this.usernameInput.value;
  }

  get password() {
    return this.passwordInput.value;
  }
}

class Parser {
  constructor(authUrl) {
    this.authUrl = authUrl;
  }

  async fetchHtml() {
    try {
      const response = await fetch(this.authUrl);
      const html = await response.text();
      return new LoginParser(html);
    } catch (error) {
      console.error(chalk.red('Error fetching authentication form:', error));
      return null;
    }
  }

  async parse() {
    const parser = await this.fetchHtml();
    if (!parser) return null;
    parser.parse();
    return parser;
  }
}

module.exports = Parser;