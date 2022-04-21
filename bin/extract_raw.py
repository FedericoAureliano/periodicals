import re

with open("data/raw/details.txt") as f:
    text = f.read()

with open("data/raw/geography.txt") as f:
    geo = f.read()

with open("data/raw/publishers.txt") as f:
    pub = f.read()

with open("data/raw/subjects.txt") as f:
    subj = f.read()

with open("data/raw/links.txt") as f:
    links = f.read()
    links = links.split("\n")

def get_link(id):
    for l in links:
        prefix = l[:l.find(" : ")]
        suffix = l[l.find("http"):]
        if prefix == str(id):
            return f"\"{suffix}\""
    return ""

MAX = 6562
LOOKAHEAD = 100

STATES = [
    "STATE Alabama STATE",
    "STATE Alaska STATE",
    "STATE Arizona STATE",
    "STATE Arkansas STATE",
    "STATE California STATE",
    "STATE Colorado STATE",
    "STATE Connecticut STATE",
    "STATE Delaware STATE",
    "STATE Florida STATE",
    "STATE Georgia STATE",
    "STATE Hawaii STATE",
    "STATE Idaho STATE",
    "STATE Illinois STATE",
    "STATE Indiana STATE",
    "STATE Iowa STATE",
    "STATE Kansas STATE",
    "STATE Kentucky STATE",
    "STATE Louisiana STATE",
    "STATE Maine STATE",
    "STATE Maryland STATE",
    "STATE Massachusetts STATE",
    "STATE Michigan STATE",
    "STATE Minnesota STATE",
    "STATE Mississippi STATE",
    "STATE Missouri STATE",
    "STATE Montana STATE",
    "STATE Nebraska STATE",
    "STATE Nevada STATE",
    "STATE New Hampshire STATE",
    "STATE New Jersey STATE",
    "STATE New Mexico STATE",
    "STATE New York STATE",
    "STATE North Carolina STATE",
    "STATE North Dakota STATE",
    "STATE Ohio STATE",
    "STATE Oklahoma STATE",
    "STATE Oregon STATE",
    "STATE Pennsylvania STATE",
    "STATE Rhode Island STATE",
    "STATE South Carolina STATE",
    "STATE South Dakota STATE",
    "STATE Tennessee STATE",
    "STATE Texas STATE",
    "STATE Utah STATE",
    "STATE Vermont STATE",
    "STATE Virginia STATE",
    "STATE Washington STATE",
    "STATE West Virginia STATE",
    "STATE Wisconsin STATE",
    "STATE Wyoming STATE",
    "STATE District of Columbia STATE",
]

with open('data/bibliography.csv', 'w') as compiled:
    print("ID,Name,First,Last,City,State,Publisher,Subject,Link", file=compiled, flush=True)

    print("ID#,Problem,Name")
    # For each ID
    for i in range(1, MAX+1):
        # Find where the word "frequency" occurs after this ID
        p = re.compile("\n%s (.|[\n])*[Ff]requency" % (i))
        find_id_and_freq = p.search(text)

        if not find_id_and_freq:
            # if we can't find the word "frequency" occuring after this ID then go to the next
            print("%d,frequency," % i, flush=True)
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
            print("%d,start date," % i, flush=True)
            continue
        if start_of_freq < 0:
            # we couldn't find a frequency, so go to the next ID
            print("%d,frequency," % i, flush=True)
            continue
        if date_dash < 0:
            # we couldn't find a dash between years, so go to the next ID
            print("%d,end date," % i, flush=True)
            continue

        name = text[start_of_id:start_of_date].replace('\n', '')

        while name.startswith(" ") or name.startswith(","):
            name = name[1:]
        while name.endswith(" ") or name.endswith(","):
            name = name[:-1]

        first = text[start_of_date:date_dash].replace(' ', '').replace('.', '').replace('-', '').replace('?', '').replace('\n', '')
        last = text[date_dash:start_of_freq].replace(' ', '').replace('.', '').replace('-', '').replace('?', '').replace('\n', '')

        if len(first) != 4:
            # start year doesn't make sense
            print("%d,start date," % i, flush=True)
            continue

        # now let's find the city and state
        r = re.compile("[\s,]%d[\s,]" % (i))
        id_in_geo = r.search(geo)

        if not id_in_geo:
            # couldn't find ID in geo, go to next ID
            print("%d,geography,\"%s\"" % (i, name), flush=True)
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
        reverse_starting_after_city = reverse_starting_at_id[city_start+len(city):]
        for s in STATES:
            state_pos = reverse_starting_after_city.find(s[::-1])
            if (state_pos > 0 and state_pos < best) or best == -1:
                state = s
                best = state_pos

        if best < 0:
            # couldn't find a state, go to next ID
            print("%d,state,\"%s\"" % (i, name), flush=True)
            continue

        # Now let's find the publisher
        id_in_pub = r.finditer(pub)

        publisher = ""

        for m in id_in_pub:
            id_start = m.start()
            reverse_starting_at_id = pub[:id_start][::-1]

            re_publisher_name = re.compile("([^\d\n]*[a-zA-Z]+[^\d\n]*)+")
            publisher_match = re_publisher_name.search(reverse_starting_at_id)
            if not publisher_match:
                # couldn't find publisher, go to next ID
                print("%d,publisher,\"%s\"" % (i, name), flush=True)
                continue

            publisher_start = publisher_match.start()
            tmp_publisher = publisher_match.group(0)[::-1].replace('\n', '')

            while tmp_publisher.startswith(" ") or tmp_publisher.startswith(","):
                tmp_publisher = tmp_publisher[1:]
            while tmp_publisher.endswith(" ") or tmp_publisher.endswith(","):
                tmp_publisher = tmp_publisher[:-1]

            publisher = tmp_publisher + " and " + publisher if publisher else tmp_publisher

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
                print("%d,topic,\"%s\"" % (i, name), flush=True)
                continue

            subject_start = subject_match.start()
            tmp_subject = subject_match.group(0)[::-1].replace('\n', '')

            while tmp_subject.startswith(" ") or tmp_subject.startswith(","):
                tmp_subject = tmp_subject[1:]
            while tmp_subject.endswith(" ") or tmp_subject.endswith(","):
                tmp_subject = tmp_subject[:-1]

            subject = tmp_subject + " | " + subject if subject else tmp_subject

        print("%d,\"%s\",%s,%s,\"%s\",\"%s\",\"%s\",\"%s\",%s" %(i, name, first, last, city, state[len("STATE "):-len(" STATE")], publisher, subject, get_link(i)), file=compiled, flush=True)