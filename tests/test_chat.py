import pytest

def test_init(activechat, testbot):
    a = activechat(0, testbot)
    assert a.chatid == 0
    assert a.state == "start"

def test_command_register(activechat, testbot):
    a = activechat(1, testbot)
    assert a.state == "start"
    a.parseMessage("/register")
    assert a.state == "register"
    assert testbot.lastmessage == "Please send me the password to subscribe."
    a.parseMessage("passw0rd")
    assert testbot.lastmessage == "This is unfortunately wrong. Please try again."
    assert a.state == "register"
    a.parseMessage("password")
    assert testbot.lastmessage == "You are now registered."
    assert a.state == "start"

def test_command_unregister(activechat, testbot):
    a = activechat(2, testbot)
    assert a.state == "start"
    a.parseMessage("/unregister")
    assert a.state == "unregister"

def test_command_cancel(activechat, testbot):
    a = activechat(3, testbot)
    assert a.state == "start"
    a.parseMessage("/cancel")
    assert a.state == "start"


def test_command_start(activechat, testbot):
    a = activechat(4, testbot)
    assert a.state == "start"
    a.parseMessage("/register")
    assert a.state == "register"
    a.parseMessage("/start")
    assert a.state == "start"


def test_metachat(activechat, testbot):
    a = activechat(8472, testbot)
    a.parseMessage("/register")
    assert a.state == "register"
    del a
    b = activechat(8472, testbot)
    assert b.state == "register"