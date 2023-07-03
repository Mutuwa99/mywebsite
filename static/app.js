class Chatbox {
  constructor() {
    this.openButton = document.querySelector('.chatbox__button');
    this.chatBox = document.querySelector('.chatbox__support');
    this.sendButton = document.querySelector('.send__button');
    this.messages = [];
  }

  display() {
    this.openButton.addEventListener('click', () => this.toggleState(this.chatBox));
    this.sendButton.addEventListener('click', () => this.onSendButton(this.chatBox));

    const node = this.chatBox.querySelector('input');
    node.addEventListener('keyup', ({ key }) => {
      if (key === 'Enter') {
        this.onSendButton(this.chatBox);
      }
    });
  }

  toggleState(chatbox) {
    this.chatBox.classList.toggle('chatbox--active');
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector('#user-input');

    let user_input = textField.value;
    console.log('this is the ' + user_input);
    if (user_input === '') {
      return;
    }

    let msg1 = ['User', user_input];
    this.messages.push(msg1);

    fetch('http://127.0.0.1:5000/chatbot', {
      method: 'POST',
      body: JSON.stringify({ message: user_input }),
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = ['Sam', r.answer];
        this.messages.push(msg2);
        this.updateChatText(chatbox);
        textField.value = '';
      })
      .catch((error) => {
        console.error('Error:', error);
        this.updateChatText(chatbox);
        textField.value = '';
      });
  }

  updateChatText(chatbox) {
    var html = '';
    this.messages.slice().reverse().forEach(function (item, index) {
      if (item[0] === 'Sam') {
        html += '<div class="messages__item messages__item--visitor">' + item[1] + '</div>';
      } else {
        html += '<div class="messages__item messages__item--operator">' + item[1] + '</div>';
      }
    });

    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();
