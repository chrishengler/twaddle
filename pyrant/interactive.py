import interpreter.interpreter as Interpreter


while True:
    sentence = input(">")
    print(Interpreter.interpret_external(sentence))
