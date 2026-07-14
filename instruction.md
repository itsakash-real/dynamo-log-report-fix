There is a file called access.log in the working directory (Apache-style
format). Parse it and write /app/report.json with three keys:

  "total_requests"  — how many non-empty lines the log contains
  "unique_ips"      — how many distinct client IPs appear
  "top_path"        — the most frequently requested URL path

The output must be valid JSON. Write the file, then stop.
