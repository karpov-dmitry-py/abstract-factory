from abc import ABC, abstractmethod
import factory

class FrameManager:

    STRIKE_SYMBOL = 'X'
    SPARE_SYMBOL = '/'
    MISS_SYMBOL = '-'

    # общее
    MAX_FRAMES = 10
    PINS_QTY = 10

    # для национальных правил
    STRIKE_POINTS = 20
    SPARE_POINTS = 15

    def __init__(self, game_result, rules: int = 1):

        this_game_factory = factory.GeneralRules.get_rules_support_info().get(rules)
        if not this_game_factory:
            raise BaseException((f'Не разработан расчет игры для вида правил с кодом <{rules}>'))

        self.game_result = str(game_result).upper()
        self.factory = this_game_factory
        self.extra_points = []
        self.spare_first_throw_points = 0

    def _get_extra_points_total(self):
        total = sum(sum(points[1]) for points in self.extra_points)
        return total

    def get_frames(self):

        if not self.game_result:
            raise ValueError(f'Передан пустой результат игры.')

        if len(self.game_result) == 1 and self.game_result != FrameManager.STRIKE_SYMBOL:
            raise ValueError('Передан неверный результат игры')

        frames = []
        frame = ''

        for char_number, char in enumerate(self.game_result, start=1):

            frame += char
            if len(frame) == 1 and char_number == len(self.game_result) and \
                    char != FrameManager.STRIKE_SYMBOL:
                raise ValueError(f'Передан неверный результат игры - см. последний фрейм: {frame}')

            if len(frame) == 2 or frame == FrameManager.STRIKE_SYMBOL:

                if (all(char.isdigit() for char in frame)
                                                   and sum(int(char) for char in frame) >= FrameManager.PINS_QTY
                ):
                    raise ValueError(f'Передан неверный результат игры - неверный фрейм: ({frame})')

                frames.append(frame)
                frame = ''

                total_frames = len(frames)
                if total_frames > FrameManager.MAX_FRAMES:
                    raise ValueError(f'Передан неверный результат игры: ({frame}) '
                                                 f'Кол-во фактических фреймов ({total_frames}) '
                                                 f'превышает разрешенное кол-во фреймов: ({FrameManager.MAX_FRAMES})')

        return frames

    def get_score(self):

        FIRST_THROW = self.factory.create_first_throw(manager=self)
        SECOND_THROW = self.factory.create_second_throw(manager=self)

        total_score = 0
        frames = self.get_frames()

        for frame in frames:

            self.spare_first_throw_points = int(frame.replace('/', '')) if \
                FrameManager.SPARE_SYMBOL in frame else 0

            frame_score = 0
            for char_number, char in enumerate(frame, start=1):
                frame_score += FIRST_THROW.process(char) if char_number == 1 else \
                    SECOND_THROW.process(char)
            total_score += frame_score

        total_score += self._get_extra_points_total()
        return {'total_frames': len(frames), 'total_score': total_score}

def main():

    # game_result = 'Х' * 9 + ''
    # game_result = 'Х4/34'
    game_result = 'XXX347/21'
    # game_result = '12345/'

    try:
        result = FrameManager(game_result).get_score()
        print(
            f"Игра: {game_result}. Всего фреймов сыграно: {result['total_frames']}. Очков набрано: {result['total_score']}")
    except BaseException as exc:
        print(f'Ошибка расчета ({exc.__class__.__name__}): {exc.args}')

if __name__ == '__main__':
    main()