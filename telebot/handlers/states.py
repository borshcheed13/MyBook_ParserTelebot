from aiogram.fsm.state import State, StatesGroup

class _FSM_Fill_Form_new_users(StatesGroup):
    '''Класс, создающий группу состояний FSM(Finite State Machine - машина состояний) для новых пользователей'''
    fill_name = State()
    fill_receive_notification = State()
    fill_view_the_books = State()
    end_of_the_survey = State()


class _FSM_Fill_Form_old_users(StatesGroup):
    '''Класс, создающий группу состояний FSM(Finite State Machine - машина состояний) для старых пользователей'''
    fill_receive_notification = State()

FSM_new_users = _FSM_Fill_Form_new_users()
FSM_old_users = _FSM_Fill_Form_old_users()