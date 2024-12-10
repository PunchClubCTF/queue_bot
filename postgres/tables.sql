-- Таблица учащихся
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    group_id INT, -- Указывает на группу, если студент в группе
    is_admin BOOLEAN DEFAULT FALSE, -- Указывает, является ли пользователь администратором
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица групп
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    member1_id INT NOT NULL UNIQUE, -- Указывает на первого участника
    member2_id INT UNIQUE,          -- Указывает на второго участника
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member1_id) REFERENCES students (id),
    FOREIGN KEY (member2_id) REFERENCES students (id)
);

-- Таблица лабораторных работ
CREATE TABLE labs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL, -- Название лабораторной работы (например, Лаба 1)
    subject VARCHAR(50) NOT NULL, -- Предмет (АИП или ЦГ)
    description TEXT -- Описание (опционально)
);

-- Таблица прогресса выполнения лабораторных работ
CREATE TABLE lab_progress (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    lab_id INT NOT NULL,
    status VARCHAR(50) NOT NULL, -- Статус (например, "Сдано", "Не сдано")
    submission_date TIMESTAMP, -- Дата сдачи (опционально)
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (lab_id) REFERENCES labs (id),
    UNIQUE (student_id, lab_id) -- Чтобы один студент не мог сдать одну лабу несколько раз
);

-- Таблица очереди на сдачу лабораторных
CREATE TABLE lab_queue (
    id SERIAL PRIMARY KEY,
    student_id INT, -- ID студента (если запись одиночная)
    group_id INT,   -- ID группы (если сдача в группе)
    lab_id INT NOT NULL, -- Лаба, которую собираются сдавать
    subject VARCHAR(50) NOT NULL, -- Предмет (АИП или ЦГ)
    queue_time TIMESTAMP NOT NULL, -- Время записи в очередь
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (group_id) REFERENCES groups (id),
    FOREIGN KEY (lab_id) REFERENCES labs (id),
    CHECK (
        (student_id IS NOT NULL AND group_id IS NULL) OR 
        (group_id IS NOT NULL AND student_id IS NULL)
    ) -- Либо студент, либо группа, но не оба сразу
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(255) NOT NULL, -- Тип действия
    details TEXT, -- Подробности о действии
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES students (id)
);

ALTER TABLE lab_queue ADD COLUMN priority INT DEFAULT 0; -- Чем выше значение, тем выше приоритет
