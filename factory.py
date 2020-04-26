# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from bowling_abstract_factory_pattern import FrameManager

class Throw(ABC):

    def __init__(self, manager):
        self.manager = manager

    def _handle_extra_points(self, result, num_add_extra_throws=0):

        if not self.manager.extra_points:
            if num_add_extra_throws:
                new_extra_throws_list = [num_add_extra_throws, []]
                self.manager.extra_points.append(new_extra_throws_list)
            return

        for throw_data in self.manager.extra_points:
            num_extra_throws = throw_data[0]
            extra_throws_gathered_points = throw_data[1]
            if len(
                    extra_throws_gathered_points) < num_extra_throws:  # собрали доп. очки с недостаточного кол-ва бросков
                extra_throws_gathered_points.append(result)

        if num_add_extra_throws:
            new_extra_throws_list = [num_add_extra_throws, []]
            self.manager.extra_points.append(new_extra_throws_list)

    def process(self, symbol):
        if symbol == FrameManager.STRIKE_SYMBOL:
            return self.strike()
        elif symbol == FrameManager.SPARE_SYMBOL:
            return self.spare()
        elif symbol == FrameManager.MISS_SYMBOL:
            return 0
        elif '1' <= symbol <= '9':
            return self.int(symbol)
        else:
            raise ValueError(f'Ошибка: неверный символ: {symbol}')

    @abstractmethod
    def int(self, symbol):
        pass

    @abstractmethod
    def strike(self):
        pass

    @abstractmethod
    def spare(self):
        pass

class GeneralRules(ABC): # абстрактная фабрика

    @abstractmethod
    def create_first_throw(self):
        pass

    @abstractmethod
    def create_second_throw(self):
        pass

    @staticmethod
    def get_rules_support_info():
        factories = {
            0: NationalRules(),
            1: InternationalRules()
        }
        return factories

class NationalRules(GeneralRules):

    def create_first_throw(self, *args, **kwargs):
        return NationalFirstThrow(*args, **kwargs)

    def create_second_throw(self, *args, **kwargs):
        return NationalSecondThrow(*args, **kwargs)

class InternationalRules(GeneralRules):

    def create_first_throw(self, *args, **kwargs):
        return InternationalFirstThrow(*args, **kwargs)

    def create_second_throw(self, *args, **kwargs):
        return InternationalSecondThrow(*args, **kwargs)

class GeneralFirstThrow(ABC):
    pass

class GeneralSecondThrow(ABC):
    pass

class NationalFirstThrow(Throw, GeneralFirstThrow):

    def strike(self):
        return FrameManager.STRIKE_POINTS

    def spare(self):
        raise ValueError(f'Ошибка: cимвол SPARE ({FrameManager.SPARE_SYMBOL}) указан в первом броске')

    def int(self, symbol):
        return int(symbol)

class NationalSecondThrow(Throw, GeneralSecondThrow):

    def strike(self):
        raise ValueError(f'Ошибка: cимвол STRIKE ({FrameManager.STRIKE_SYMBOL}) указан во втором броске')

    def spare(self):
        return FrameManager.SPARE_POINTS - self.manager.spare_first_throw_points

    def int(self, symbol):
        return int(symbol)

class InternationalFirstThrow(GeneralFirstThrow, Throw):

    def strike(self):
        result = FrameManager.PINS_QTY
        self._handle_extra_points(result, 2)
        return result

    def spare(self):
        raise ValueError(f'Ошибка: cимвол SPARE ({FrameManager.SPARE_SYMBOL}) указан в первом броске')

    def int(self, symbol):
        result = int(symbol)
        self._handle_extra_points(result)
        return result

class InternationalSecondThrow(GeneralSecondThrow, Throw):

    def strike(self):
        raise ValueError(f'Ошибка: cимвол STRIKE ({FrameManager.STRIKE_SYMBOL}) указан во втором броске')

    def spare(self):

            result = FrameManager.PINS_QTY - self.manager.spare_first_throw_points
            self._handle_extra_points(result, 1)
            return result

    def int(self, symbol):
        result = int(symbol)
        self._handle_extra_points(result)
        return result

