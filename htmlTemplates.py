css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #FFFFF0
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message.bot .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #000;
}
.chat-message.user .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.youtube.com%2FStyleCraze&psig=AOvVaw26EBacYOZipX1Mg9LuC9i3&ust=1692341395233000&source=images&cd=vfe&opi=89978449&ved=0CBAQjRxqFwoTCKCpkI-N44ADFQAAAAAdAAAAABAE" style="max-height: 78px; max-width: 78px; border-radius: 20%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://t3.ftcdn.net/jpg/00/24/55/82/360_F_24558278_Ugh6eX7m225qB5SDtX5shMFhfpPPHzFc.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
