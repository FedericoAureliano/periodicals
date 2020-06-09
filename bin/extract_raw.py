import re

with open("data/raw/details.txt") as f:
    text = f.read()

with open("data/raw/geography.txt") as f:
    geo = f.read()

with open("data/raw/publishers.txt") as f:
    pub = f.read()

with open("data/raw/subjects.txt") as f:
    subj = f.read()

MAX = 6562
LOOKAHEAD = 100

STATES = [
    "Alabama STATE",
    "Alaska STATE",
    "Arizona STATE",
    "Arkansas STATE",
    "California STATE",
    "Colorado STATE",
    "Connecticut STATE",
    "Delaware STATE",
    "Florida STATE",
    "Georgia STATE",
    "Hawaii STATE",
    "Idaho STATE",
    "Illinois STATE",
    "Indiana STATE",
    "Iowa STATE",
    "Kansas STATE",
    "Kentucky STATE",
    "Louisiana STATE",
    "Maine STATE",
    "Maryland STATE",
    "Massachusetts STATE",
    "Michigan STATE",
    "Minnesota STATE",
    "Mississippi STATE",
    "Missouri STATE",
    "Montana STATE",
    "Nebraska STATE",
    "Nevada STATE",
    "New Hampshire STATE",
    "New Jersey STATE",
    "New Mexico STATE",
    "New York STATE",
    "North Carolina STATE",
    "North Dakota STATE",
    "Ohio STATE",
    "Oklahoma STATE",
    "Oregon STATE",
    "Pennsylvania STATE",
    "Rhode Island STATE",
    "South Carolina STATE",
    "South Dakota STATE",
    "Tennessee STATE",
    "Texas STATE",
    "Utah STATE",
    "Vermont STATE",
    "Virginia STATE",
    "Washington STATE",
    "West Virginia STATE",
    "Wisconsin STATE",
    "Wyoming STATE",
    "District of Columbia STATE",
]

with open('data/bibliography.csv', 'w') as compiled:
    print("ID,Name,First,Last,City,State,Publisher,Subject,Link", file=compiled)

    # For each ID
    for i in range(1, MAX+1):
        # Find where the word "frequency" occurs after this ID
        p = re.compile("\n%s (.|[\n])*[Ff]requency" % (i))
        find_id_and_freq = p.search(text)

        if not find_id_and_freq:
            # if we can't find the word "frequency" occuring after this ID then go to the next
            continue

        start_of_id   = find_id_and_freq.start() + len(" %d " %i)
        start_of_date = text.find(". 1", start_of_id, start_of_id+LOOKAHEAD)
        if start_of_date < 0:
            start_of_date = text.find("\n1", start_of_id, start_of_id+LOOKAHEAD)

        start_of_freq = text.find("Frequency", start_of_id, start_of_id+LOOKAHEAD)
        if start_of_freq < 0:
            start_of_freq = text.find("frequency", start_of_id, start_of_id+LOOKAHEAD)

        date_dash = text.find("-", start_of_date, start_of_date+LOOKAHEAD)

        if start_of_date < 0:
            # we couldn't find a date, so go to the next ID
            continue
        if start_of_freq < 0:
            # we couldn't find a frequency, so go to the next ID
            continue
        if date_dash < 0:
            # we couldn't find a dash between years, so go to the next ID
            continue

        name = text[start_of_id:start_of_date].replace('\n', '')

        while name.startswith(" ") or name.startswith(","):
            name = name[1:]
        while name.endswith(" ") or name.endswith(","):
            name = name[:-1]

        first = text[start_of_date:date_dash].replace(' ', '').replace('.', '').replace('-', '').replace('?', '').replace('\n', '')
        last = text[date_dash:start_of_freq].replace(' ', '').replace('.', '').replace('-', '').replace('?', '').replace('\n', '')

        # now let's find the city and state
        r = re.compile("[\s,]%d[\s,]" % (i))
        id_in_geo = r.search(geo)

        if not id_in_geo:
            # couldn't find ID in geo, go to next ID
            continue

        id_start = id_in_geo.start()
        reverse_starting_at_id = geo[:id_start][::-1]

        re_city_name = re.compile("([^\d\n,]*[a-zA-Z]+[^\d\n,]*)+")
        city_match = re_city_name.search(reverse_starting_at_id)
        city_start = city_match.start()
        city = city_match.group(0)[::-1].replace('\n', '')

        while city.startswith(" ") or city.startswith(","):
            city = city[1:]
        while city.endswith(" ") or city.endswith(","):
            city = city[:-1]

        best = -1
        state = ""
        for s in STATES:
            reverse_starting_after_city = reverse_starting_at_id[city_start+len(city):]
            state_pos = reverse_starting_after_city.find(s[::-1])
            if (state_pos > 0 and state_pos < best) or best == -1:
                state = s
                best = state_pos

        if best < 0:
            # couldn't find a state, go to next ID
            continue

        # Now let's find the publisher
        id_in_pub = r.search(pub)

        if not id_in_pub:
            # couldn't find ID in pub, go to next ID
            continue

        id_start = id_in_pub.start()
        reverse_starting_at_id = pub[:id_start][::-1]

        re_publisher_name = re.compile("([^\d\n]*[a-zA-Z]+[^\d\n]*)+")
        publisher_match = re_publisher_name.search(reverse_starting_at_id)
        if not publisher_match:
            # couldn't find publisher, go to next ID
            continue

        publisher_start = publisher_match.start()
        publisher = publisher_match.group(0)[::-1].replace('\n', '')

        while publisher.startswith(" ") or publisher.startswith(","):
            publisher = publisher[1:]
        while publisher.endswith(" ") or publisher.endswith(","):
            publisher = publisher[:-1]

        # Now let's find the subject
        id_in_subj = r.finditer(subj)

        subject = ""

        for m in id_in_subj:
            id_start = m.start()
            reverse_starting_at_id = subj[:id_start][::-1]

            re_subject_name = re.compile("([^\d\n]*[a-zA-Z]+[^\d\n]*)+")
            subject_match = re_subject_name.search(reverse_starting_at_id)
            if not subject_match:
                # couldn't find subject, go to next ID
                continue

            subject_start = subject_match.start()
            tmp_subject = subject_match.group(0)[::-1].replace('\n', '')

            while tmp_subject.startswith(" ") or tmp_subject.startswith(","):
                tmp_subject = tmp_subject[1:]
            while tmp_subject.endswith(" ") or tmp_subject.endswith(","):
                tmp_subject = tmp_subject[:-1]

            subject = tmp_subject + " | " + subject if subject else tmp_subject

        if subject == "":
            continue

        print("%d,\"%s\",%s,%s,\"%s\",\"%s\",\"%s\",\"%s\"," %(i, name, first, last, city, state[:-len(" STATE")], publisher, subject), file=compiled)