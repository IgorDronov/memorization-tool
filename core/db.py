from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    box = Column(Integer, default=1)


class DBManipulator:
    def __init__(self, db_url='sqlite:///flashcard.db', echo=False):
        self.engine = create_engine(db_url, echo=echo)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_flashcards(self, question: str, answer: str) -> None:
        with self.Session() as session:
            new_card = Flashcard(question=question, answer=answer)
            session.add(new_card)
            session.commit()

    def get_flashcards(self):
        with self.Session() as session:
            return session.query(Flashcard).all()

    def update_question(self, old_data, new_data):
        with self.Session() as session:
            card = session.query(Flashcard).filter(Flashcard.question == old_data).first()
            card.question = new_data
            session.commit()

    def update_answer(self, old_data, new_data):
        with self.Session() as session:
            card = session.query(Flashcard).filter(Flashcard.answer == old_data).first()
            card.answer = new_data
            session.commit()

    def update_box(self, flashcard, status):
        with self.Session() as session:
            card = session.query(Flashcard).filter(Flashcard.question == flashcard.question).first()
            new_box_number = self.get_nex_box_number(card.box, status)
            if new_box_number > 3:
                session.delete(card)
            else:
                card.box = new_box_number
            session.commit()

    @staticmethod
    def get_nex_box_number(box_number, status):
        if status:
            return box_number + 1
        else:
            if box_number == 1:
                return 1
            else:
                return box_number - 1

    def delete_flashcard(self, flashcard):
        with self.Session() as session:
            session.query(Flashcard).filter(Flashcard.id == flashcard.id).delete()
            session.commit()
