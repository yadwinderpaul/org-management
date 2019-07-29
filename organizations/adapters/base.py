from abc import ABCMeta, abstractmethod


class BaseAdapter(metaclass=ABCMeta):
    @abstractmethod
    def list_organizations(self):
        pass

    @abstractmethod
    def create_organizations(self):
        pass

    @abstractmethod
    def update_organizations(self):
        pass

    @abstractmethod
    def delete_organizations(self):
        pass

    @abstractmethod
    def search_organizations(self):
        pass
