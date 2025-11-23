class UserIsBusyException(Exception):
    message = 'Пользователь с этим id занят'


class UserNotFoundException(Exception):
    message = 'Такого пользователя не существует'


class LoginAlreadyExistsException(Exception):
    message = 'Такой email уже существует'
