import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

# Константы для правил игры
MIN_NEIGHBOURS_TO_SURVIVE = 2
MAX_NEIGHBOURS_TO_SURVIVE = 3
NEIGHBOURS_TO_REPRODUCE = 3


class GameOfLife:
    """
    Класс для реализации игры "Жизнь" Конвея.
    
    Правила игры:
    - Живая клетка с 2-3 соседями выживает, иначе умирает
    - Мертвая клетка с 3 соседями оживает
    """

    def __init__(
        self, 
        size: tp.Tuple[int, int], 
        randomize: bool = True, 
        max_generations: tp.Optional[float] = float("inf")
    ) -> None:
        """
        Инициализация игры.
        
        Parameters
        ----------
        size : Tuple[int, int]
            Размер игрового поля (rows, cols)
        randomize : bool
            Если True, создается случайное начальное состояние
        max_generations : Optional[float]
            Максимальное количество поколений (по умолчанию бесконечно)
        """
        if size[0] <= 0 or size[1] <= 0:
            raise ValueError("Размеры поля должны быть положительными числами")
        
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        
        Parameters
        ----------
        randomize : bool
            Если True, клетки заполняются случайными значениями (0 или 1)
            
        Returns
        -------
        Grid
            Двумерный список клеток
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0] * self.cols for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        -------
        Cells
            Список значений соседних клеток (0 или 1)
        """
        x, y = cell
        neighbours = []
        
        # Проверяем все 8 соседних клеток
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue  # Пропускаем саму клетку
                
                nx, ny = x + dx, y + dy
                # Проверяем границы поля
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    neighbours.append(self.curr_generation[nx][ny])
        
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток согласно правилам игры "Жизнь".

        Returns
        -------
        Grid
            Новое поколение клеток
        """
        new_grid = [[0] * self.cols for _ in range(self.rows)]

        for x in range(self.rows):
            for y in range(self.cols):
                neighbours = self.get_neighbours((x, y))
                live_neighbours = sum(neighbours)
                current_cell = self.curr_generation[x][y]
                
                # Применяем правила игры
                if current_cell == 1:
                    # Живая клетка выживает, если у нее 2-3 соседа
                    if MIN_NEIGHBOURS_TO_SURVIVE <= live_neighbours <= MAX_NEIGHBOURS_TO_SURVIVE:
                        new_grid[x][y] = 1
                else:
                    # Мертвая клетка оживает, если у нее ровно 3 соседа
                    if live_neighbours == NEIGHBOURS_TO_REPRODUCE:
                        new_grid[x][y] = 1
        
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры (переход к следующему поколению).
        """
        self.prev_generation = [row[:] for row in self.curr_generation]  # Глубокое копирование
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        
        Returns
        -------
        bool
            True, если достигнут лимит поколений, иначе False
        """
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        
        Оптимизированная версия: сравнивает клетки поэлементно и останавливается
        при первом различии для лучшей производительности.
        
        Returns
        -------
        bool
            True, если состояние изменилось, иначе False
        """
        # Быстрая проверка: если размеры не совпадают, то точно изменилось
        if len(self.prev_generation) != len(self.curr_generation):
            return True
        
        # Поэлементное сравнение с ранним выходом
        for i in range(self.rows):
            if len(self.prev_generation[i]) != len(self.curr_generation[i]):
                return True
            for j in range(self.cols):
                if self.prev_generation[i][j] != self.curr_generation[i][j]:
                    return True
        
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        
        Формат файла: каждая строка представляет строку сетки,
        где '0' - мертвая клетка, '1' - живая клетка.
        
        Parameters
        ----------
        filename : pathlib.Path
            Путь к файлу с начальным состоянием
            
        Returns
        -------
        GameOfLife
            Экземпляр игры с загруженным состоянием
            
        Raises
        ------
        FileNotFoundError
            Если файл не найден
        ValueError
            Если формат файла некорректен
        """
        try:
            with open(filename, encoding="utf-8") as f:
                grid = []
                for line_num, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue  # Пропускаем пустые строки
                    
                    row = []
                    for char in line:
                        if char not in '01':
                            raise ValueError(
                                f"Неверный символ '{char}' в строке {line_num}. "
                                f"Ожидаются только '0' и '1'"
                            )
                        row.append(int(char))
                    
                    if row:
                        grid.append(row)
            
            if not grid:
                raise ValueError("Файл пуст или содержит только пустые строки")
            
            # Проверяем, что все строки имеют одинаковую длину
            cols = len(grid[0])
            for i, row in enumerate(grid, start=1):
                if len(row) != cols:
                    raise ValueError(
                        f"Строка {i} имеет длину {len(row)}, "
                        f"ожидалась длина {cols}"
                    )
            
            rows = len(grid)
            game = GameOfLife((rows, cols), randomize=False)
            game.curr_generation = grid
            return game
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{filename}' не найден")
        except IOError as e:
            raise IOError(f"Ошибка при чтении файла '{filename}': {e}")

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        
        Формат файла: каждая строка представляет строку сетки,
        где '0' - мертвая клетка, '1' - живая клетка.
        
        Parameters
        ----------
        filename : pathlib.Path
            Путь к файлу для сохранения
            
        Raises
        ------
        IOError
            Если произошла ошибка при записи файла
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for row in self.curr_generation:
                    f.write("".join(str(cell) for cell in row) + "\n")
        except IOError as e:
            raise IOError(f"Ошибка при записи файла '{filename}': {e}")
