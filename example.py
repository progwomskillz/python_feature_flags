from python_feature_flags import FeatureFlags


feature_flags = FeatureFlags(['feature_login', 'feature_logout'])


class AuthService():
    @feature_flags.feature_flag('feature_login')
    def login(self):
        return 'Hello from class AuthService method login()'

    @feature_flags.feature_flag('feature_logout')
    def logout(self):
        return 'Hello from class AuthService method logout()'

auth_service = AuthService()
print(f'auth_service.login(): {auth_service.login()}') # Hello from class AuthService method login()
print(f'auth_service.logout(): {auth_service.logout()}') # None
