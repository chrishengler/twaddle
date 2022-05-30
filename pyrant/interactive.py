import interpreter.interpreter as interpreter


while True:
    sentence = input(">")
    print(interpreter.interpret_external(sentence))
