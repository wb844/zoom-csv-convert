import sys
import csv

def license_parse(input_license):
    return_license = {}

    if "Licensed" in input_license:
        return_license["User Type"] = "Licensed"
    elif "On-Prem" in input_license:
        return_license["User Type"] = "On-Prem"
    else:
        return_license["User Type"] = "Basic"

    license_string = input_license[input_license.find("(")+1:input_license.find(")")]
    if license_string:
        license_list = license_string.split("|")
        webinar_license = [i for i in license_list if "Zoom Webinars" in i]
        events_license = [i for i in license_list if "Zoom Events" in i]
        whiteboard_license = [i for i in license_list if "Zoom Whiteboard" in i]
        large_license = [i for i in license_list if "Large" in i]
        cmk_license = [i for i in license_list if "Zoom Customer Manged Key" in i]

        if webinar_license:
            return_license["Zoom Webinars"] = webinar_license[0]
        if events_license:
            return_license["Zoom Events"] = events_license[0]
        if whiteboard_license:
            return_license["Zoom Whiteboard"] = whiteboard_license[0]
        if large_license:
            return_license["Large Meeting"] = large_license[0]
        if cmk_license:
            return_license["Zoom Customer Managed Key"] = cmk_license[0]

    return return_license

with open("zoom_sample_update_users.csv", encoding='utf-8-sig') as sample_file:
    sample_reader = csv.DictReader(sample_file, delimiter=",")

    field_names = next(sample_reader).keys()

with open(sys.argv[1], encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    with open(sys.argv[2], mode='w') as write_file:
        csv_writer = csv.DictWriter(write_file, fieldnames=field_names, extrasaction="ignore", delimiter=',')

        csv_writer.writeheader()
        for row in csv_reader:

            if "(Zoom Rooms)" in row["Email"] :
                continue
            license = row["License Type"]
            license_object = license_parse(license)
            row.update(license_object)

            csv_writer.writerow(row)
            line_count += 1

    print("Output {} lines!".format(line_count))
