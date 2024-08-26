package org.cloudfoundry.samples.music.domain;

public class MessageRequest {
    private Message[] messages;

    public MessageRequest() {
        
    }

    public MessageRequest(Message[] messages) {
        this.messages = messages;
    }

    public Message[] getMessages() {
        return this.messages;
    }

    public void setMessages(Message[] messages) {
        this.messages = messages;
    }
}
