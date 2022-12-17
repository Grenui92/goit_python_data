from abc import abstractmethod, ABC

class MainMethods(ABC):

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def add_values(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def delete_all(self):
        raise NotImplemented

    @abstractmethod
    def delete_one(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def load_from_file(self):
        raise  NotImplemented

    @abstractmethod
    def save_to_file(self):
        raise NotImplemented

    @abstractmethod
    def edit_information(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def edit_name(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def search_in(self, *args, **kwargs):
        raise NotImplemented

class ShowMethods(ABC):
    @abstractmethod
    def show_all(self):
        raise NotImplemented

    @abstractmethod
    def show_one(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def show_page(self, *args, **kwargs):
        raise NotImplemented





