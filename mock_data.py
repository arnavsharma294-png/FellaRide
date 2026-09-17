"""Mock social-signal data used by the FellaRide prototype."""

import pandas as pd


def generate_mock_posts() -> pd.DataFrame:
    """Return twenty representative posts from a target university subreddit."""
    posts = [
        ("u/parkedagain", "Paid ₹150 to park near the library and still walked 15 minutes. Anyone commuting from Govindapura want to split rides?", 84, "Govindapura"),
        ("u/late_to_lab", "The 7:40 bus was delayed again and I missed the start of my lab. Campus transit needs help.", 63, "Rajarajeshwari Nagar"),
        ("u/hack_builder", "Going to the Friday Hackathon? I have two open seats from Church Street and can leave at 5:30.", 112, "Church Street"),
        ("u/commuterclub", "We should make a commuter group for everyone coming from Koramangla—parking passes are impossible this semester.", 96, "Koramangla"),
        ("u/greenquad", "Who else is headed to the Friday Hackathon from Rajarajeshwari Nagar? Let’s coordinate instead of all ordering rides alone.", 77, "Rajarajeshwari Nagar"),
        ("u/bus_stop_blues", "Route 12 was 25 minutes late in the rain. I would happily ride with someone from Govindapura on Tuesdays and Thursdays.", 58, "Govindapura"),
        ("u/garagefull", "The Kadugodi parking area filled before 9 a.m. again. Is there any reliable way to share a parking commute?", 71, "Kadugodi"),
        ("u/designsprint", "Our design club is bringing a crew to Friday Hackathon. If anyone has a car, reply and we can organize pickups.", 89, "Rajajinagar"),
        ("u/quietreader", "Does anyone know whether the library is open later during midterms?", 21, "Kempegowda Bus Station"),
        ("u/eastside_driver", "I drive past campus from Church Street every weekday around 8:15 and hate seeing empty seats in my car.", 66, "Church Street"),
        ("u/transit_tired", "Missed my connection because the shuttle tracker said ‘arriving’ for 12 minutes. Looking for a carpool from Koramangla.", 74, "Koramangla"),
        ("u/club_president", "I can share a Friday Hackathon carpool post with the coding club and Rajarajeshwari Nagar group chats if someone starts one.", 105, "Rajarajeshwari Nagar"),
        ("u/campuscoffee", "Parking ticket warning near the student union today—heads up, they are checking every row.", 44, "Kadugodi"),
        ("u/fridayroadtrip", "Need a ride to Friday Hackathon from Govindapura; happy to chip in for gas and snacks.", 81, "Govindapura"),
        ("u/night_shift", "The late bus after my campus job has been unreliable. Any evening commuters from Rajajinagar?", 49, "Rajajinagar"),
        ("u/ride_organizer", "I know people in the robotics, debate, and CS groups. Tag me if you are coordinating rides to Friday Hackathon.", 118, "Church Street"),
        ("u/parkingmath", "Between gas and parking I’m spending way too much just to get to class. Would share rides from Kadugodi.", 69, "Kadugodi"),
        ("u/firstyear", "New here—what is the least stressful way to get from Kempegowda Bus Station to the Friday Hackathon venue?", 55, "Kempegowda Bus Station"),
        ("u/vanpool_idea", "Could we match people by neighborhood for the hackathon? I can ask our Koramangla student org leaders to spread the word.", 101, "Koramangla"),
        ("u/commute_win", "Carpooled with two classmates this week and skipped the garage chaos. Highly recommend it for anyone in Rajajinagar.", 61, "Rajajinagar"),
    ]
    return pd.DataFrame(posts, columns=["Username", "Post_Text", "Upvotes", "Stated_Location"])
