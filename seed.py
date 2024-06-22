from app import db, create_app
from app.models import Drone, Task

app = create_app()


def create_dummy_data():
    db.drop_all()
    db.create_all()

    drone_names = ['Bayraktar', 'ANKA', 'Akıncı', 'Aksungur', 'Alpha', 'Beta', 'Gamma', 'Delta']
    drones = [Drone(name=name) for name in drone_names]
    db.session.add_all(drones)
    db.session.commit()

    tasks = [
        Task(
            name='Survey Area A',
            description='Conduct a survey of Area A to collect aerial images.',
            drone_id=drones[0].id
        ),
        Task(
            name='Inspect Power Lines',
            description='Inspect the power lines in sector 4 for maintenance issues.',
            drone_id=drones[1].id
        ),
        Task(
            name='Monitor Wildlife',
            description='Monitor the wildlife in the nature reserve for research purposes.',
            drone_id=drones[2].id
        ),
        Task(
            name='Traffic Monitoring',
            description='Monitor the traffic flow at the main intersection during rush hour.',
            drone_id=drones[3].id
        )
    ]
    db.session.add_all(tasks)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        create_dummy_data()
        print("Database has been seeded.")
