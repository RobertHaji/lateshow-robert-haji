import random
from model import db, Episode, Guest, Appearance
from app import app

# Sample data (paste the large guest list into this variable or import from a file)
guest_data = [
    # Format: (date, occupation, name)
    ("1/11/99", "actor", "Michael J. Fox"),
    ("1/12/99", "Comedian", "Sandra Bernhard"),
    ("1/13/99", "television actress", "Tracey Ullman"),
    ("1/14/99", "film actress", "Gillian Anderson"),
    ("2/10/99", "actress", "Pamela Anderson, Natalie Raitano, Molly Culver"),
    # ⬆️ Add the rest of your data here in the same format
]


def parse_date_to_number(date_str):
    # Example: '1/11/99' → 19990111
    mm, dd, yy = date_str.split("/")
    return int(f"1999{int(mm):02}{int(dd):02}")


def seed():
    with app.app_context():
        # Clear existing data
        Appearance.query.delete()
        Episode.query.delete()
        Guest.query.delete()

        db.session.commit()

        date_to_episode = {}
        name_to_guest = {}

        for entry in guest_data:
            date, occupation, name_str = entry
            number = parse_date_to_number(date)

            # Create or get Episode
            if date not in date_to_episode:
                episode = Episode(date=date, number=number)
                db.session.add(episode)
                date_to_episode[date] = episode
            else:
                episode = date_to_episode[date]

            # Some entries have multiple guests (e.g., joined by commas)
            names = [n.strip() for n in name_str.split(",")]

            for guest_name in names:
                # Create or get Guest
                if guest_name not in name_to_guest:
                    guest = Guest(
                        name=guest_name,
                        occupation=occupation if occupation != "NA" else None,
                    )
                    db.session.add(guest)
                    name_to_guest[guest_name] = guest
                else:
                    guest = name_to_guest[guest_name]

                # Create Appearance with a random rating
                rating = random.randint(1, 5)
                appearance = Appearance(
                    guest=guest,
                    episode=episode,
                    rating=rating,
                )
                db.session.add(appearance)

        db.session.commit()
        print("Seeded successfully!")


if __name__ == "__main__":
    seed()
