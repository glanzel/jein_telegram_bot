from sqlalchemy import func
from base import Session, Base
from reactions import Reactions

session = Session()
#select = session.query(Reactions).filter(Reactions.message_id == "AgAAAAnzAQD5tOkF7iFTdx0XVEk")
select = session.query(Reactions.value, func.count(Reactions.value)).filter(Reactions.message_id== "AgAAAAnzAQD5tOkF7iFTdx0XVEk").group_by(Reactions.value)

for row in select:
    print(row)
