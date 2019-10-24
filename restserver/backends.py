from hashlib import sha1

from .models import User


class Opencurtainbackend:
    def authenticate(self, username=None, password=None):
        try:
            hashed = sha1(
                (user.salt + sha1(
                    (user.salt + sha1(
                        password.encode('utf8')
                    ).hexdigest()).encode('utf8')
                ).hexdigest()).encode('utf8')
            ).hexdigest()
#예시코드의 암호화방식을 그대로 적어놓았음!
            if user.password == hashed:
                return user
            else:
                return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_email):
        try:
            return User.objects.get(pk=user_email)
        except User.DoesNotExist:
            return None