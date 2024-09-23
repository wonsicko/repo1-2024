import csv
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def populate_data(filename):


   # Get CSV file path
   csv_file = os.path.join(dir_path, filename)

   # Open the CSV file and extract the data
   with open(csv_file, newline='', encoding='utf-8') as file:
       reader = csv.reader(file)
       data = list(reader)

   # Extract the data from the CSV
   meet_name = data[0][0]  # Column A - h1 (Meet Name)
   meet_date = data[1][0]  # Column B - h2 (Meet Date)
   team_results_link = data[2][0]  # Column C - hyperlink for the team-results section
   # folder_name = data[1][3]  # Column D - folder name used in photo-gallery links
   race_comments = "".join(data[3])  # Column E - race-comments section
   team_place = data[13][0]

   # retrieve number of runners from Skyline
   athletes = []
   num_of_runners = 0
   for row in data[26:]:
       if (len(row) > 4) and (row[5] == "Ann Arbor Skyline"):
           num_of_runners += 1
           athletes.append(row)
       else:
           continue

   # Create list of athlete race times
   times = []
   for athlete in athletes:
       time = athlete[4]
       times.append(time)

  # Function to convert time in 'mm:ss.sss' format to total seconds
   def time_to_seconds(time_str):
       minutes, seconds = time_str.split(':')
       total_seconds = (int(minutes) * 60) + float(seconds)
       return total_seconds

  # Convert all times to seconds
   times_in_seconds = [time_to_seconds(time) for time in times]

  # Calculate the average time in seconds
   average_time_seconds = sum(times_in_seconds) / len(times_in_seconds)

  # Convert the average time back to minutes and seconds
   def seconds_to_time(total_seconds):
       minutes = int(total_seconds // 60)
       seconds = total_seconds % 60
       return f"{minutes}:{seconds:.2f}"

  # Distance of the race (miles)
   distance_miles = 3.1

  # Calculate the average pace per mile (total seconds per mile)
   average_pace_per_mile_seconds = average_time_seconds / distance_miles

  # Convert the average pace per mile back to minutes and seconds
   average_pace_per_mile = seconds_to_time(average_pace_per_mile_seconds)

  # Sort athletes by time (convert to seconds for sorting)
   athletes_sorted = sorted(athletes, key=lambda x: time_to_seconds(x[4]))

   # Get the times for the top 3 athletes
   top_three_times = [time_to_seconds(athlete[4]) for athlete in athletes_sorted[:3]]

   # Calculate the average time for the top 3 athletes in seconds
   average_top_three_seconds = sum(top_three_times) / len(top_three_times)

   # Calculate the average pace per mile for the top 3 athletes
   average_top_three_pace_per_mile_seconds = average_top_three_seconds / distance_miles

   # Convert the average pace per mile for the top 3 back to minutes and seconds
   average_top_three_pace_per_mile = seconds_to_time(average_top_three_pace_per_mile_seconds)

   # Set image folder to correct event 
   if "bath" in filename.lower():
       image_folder = "bath"
   elif "early" in filename.lower():
       image_folder = "earlybird"
   elif "sec" in filename.lower():
       image_folder = "sec1"
   else:
       image_folder = "sec1"


   # Start building the HTML structure
   html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meet_name}</title>
</head>
<body>


<header>
<h1>{meet_name}</h1>
<p class="header-info">Date: {meet_date} | Location: ...</p>
<p><a href="{team_results_link}">See All Results</a></p>
</header>


<!-- Section for photo gallery -->
<section id="photo-gallery">
<h2>Photo Gallery</h2>
<div class="gallery">
  <div class="gallery-item">
    <img src="images/{image_folder}/{athletes[0][2].split(" ")[0]}.jpg" alt="{athletes[0][2]}">
  </div>
  <div class="gallery-item">
    <img src="images/{image_folder}/{athletes[1][2].split(" ")[0]}.jpg" alt="{athletes[1][2]}">
  </div>
  <div class="gallery-item">
    <img src="images/{image_folder}/{athletes[2][2].split(" ")[0]}.jpg" alt="{athletes[2][2]}">
  </div>
</div>
</section>


<!-- Section for overall team results -->
<section id="overall-team-results">
<h2>Overall Team Results</h2>
<table class="team-results-table">
  <tr>
    <th>Place</th>
    <td>{team_place}</td>
  </tr>
  <tr>
    <th>Total Runners</th>
    <td>{num_of_runners}</td>
  </tr>
   <tr>
    <th>Average Pace</th>
    <td>{average_pace_per_mile}</td>
  </tr>
  <tr>
    <th>Top 3 Average Pace</th>
    <td>{average_top_three_pace_per_mile}</td>
  </tr>
</table>
</section>

<!-- Section for athlete results -->
<section id="athlete-results">
<h2>Athlete Results</h2>
<table class="athlete-results-table">
  <tr>
    <th>Name</th>
    <th>Place</th>
    <th>Grade</th>
    <th>Time</th>
  </tr>'''
   for athlete in athletes:
      html_content += f'''<tr>
    <td>{athlete[2]}</td>
    <td>{athlete[0].strip(".")}</td>
    <td>{athlete[1]}</td>
    <td>{athlete[4]}</td>
    </tr>'''

   html_content += f'''
   </table>
   </section>
   <!-- Section for Coach comments -->
<section id="coach-comments">
<h2>Comments from the Coach</h2>
<p>{race_comments}</p>
</section>

</body>
</html>'''

   output_file = "-".join(meet_name.split(" ")) + ".html"
   with open(output_file, 'w') as file:
       file.write(html_content)

   return html_content

directory = dir_path + "/meets"
files = []

# iterate over files in that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    files.append(f)

# print(files)

for file in files:
    populate_data(file)

