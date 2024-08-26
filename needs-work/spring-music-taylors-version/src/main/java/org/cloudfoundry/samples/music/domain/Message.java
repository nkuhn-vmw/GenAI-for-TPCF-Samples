package org.cloudfoundry.samples.music.domain;

public class Message {
    private String role;
    private String text;

    public Message(String role, String text) {
        this.role = role;
        this.text = text;
    }

    public String getRole() {
        return this.role;
    }

    public String getText() {
        return this.text;
    }
}
