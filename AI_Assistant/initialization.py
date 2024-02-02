from setting import db
from tables import Answers


def init_database():
    """ initialization of database tables and data """
    db.drop_all()
    db.create_all()   # create all tables
    listening_answers_list=[["Jamieson","afternoon","communication","week","10","suit","passport","personality","feedback","time"],['A','B','A','C','river','1422','top','pass','steam','capital'],['G','F','A','E','B','C','C','A','B','D'],['shelter','oil','roads','insects','grass','water','soil','dry','simple','nests']]
    reading_answers_list=[['oval','husk','seed','mace','FALSE','NOT GIVEN','TRUE','Arabs','plague','lime','Run','Mauritius','tsunami'],['C','B','E','G','D','human error','car-sharing','ownership','mileage','C','D','A','E'],['A','C','C','D','A','B','E','A','D','E','B','expeditions','isolated','land surface']]

    for i in range(0,4): # initialize the info for the test answers
        model_answer = Answers()
        model_answer.practice_name = "listening"+str(i+1)
        model_answer.content = str(listening_answers_list[i])
        db.session.add(model_answer)
        db.session.commit()

    for i in range(0,3): # initialize the info for the test answers
        model_answer = Answers()
        model_answer.practice_name = "reading"+str(i+1)
        model_answer.content = str(reading_answers_list[i])
        db.session.add(model_answer)
        db.session.commit()
