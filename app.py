from flask import Flask, render_template, request

app = Flask(__name__)

POSTS = [
    {
        "title": "New Python Flask site",
        "date": "Jun 15, 2026",
        "body": "A challenge over the weekend converting my old blog to a Flask app running in Docker and GitHub Actions. Lots more work to do but so far it's been fun making this secure and publicly visable, using GitHub workflows, migrating the old HTML/JS code to Flask/Jinja and setting up Docker on the Linode Akamai Arch VM.",
        "images": [],
    },
    {
        "title": "Lake Georgetown Goodwater Loop",
        "date": "Sep 25, 2021",
        "body": "The Dragon is still my most challenging local ride. 28 miles in four hours. It's always an accomplishment.",
        "images": [
            {"src": "https://www.bevilacqua.us/img/LG0.jpg", "alt": "Lake Georgetown"},
            {"src": "https://www.bevilacqua.us/img/LG2.jpg", "alt": "Lake Georgetown"},
            {"src": "https://www.bevilacqua.us/img/LG1.jpg", "alt": "Lake Georgetown"},
        ],
    },
    {
        "title": "Reveille Peak Ranch",
        "date": "Sep 18, 2021",
        "body": None,
        "images": [
            {"src": "https://www.bevilacqua.us/img/RPR0.jpg", "alt": "Reveille Peak Ranch"},
            {"src": "https://www.bevilacqua.us/img/RPR1.jpg", "alt": "Reveille Peak Ranch"},
        ],
    },
    {
        "title": "Matthew on his first bicycle",
        "date": "Sep 12, 2021",
        "body": None,
        "images": [
            {"src": "https://www.bevilacqua.us/img/mlb-9-12-21.jpg", "alt": "Matthew on his first bicycle"},
        ],
    },
    {
        "title": "MTB at Brushy Creek",
        "date": "Sep 11, 2021",
        "body": None,
        "images": [
            {"src": "https://www.bevilacqua.us/img/bc-9-21-sm.jpg", "alt": "MTB at Brushy Creek"},
        ],
    },
    {
        "title": "New Beginnings",
        "date": "Jul 26, 2021",
        "body": "I accepted a position as a Principal Network Monitoring Engineer with Oracle Corp. This is a significant step forward in my career. I found myself needing new challenges after spending eleven years in the cable industry. I am grateful to be a part of the cloud services team. And excited that I will bring decades of experience along with me in this new endeavor.",
        "images": [],
    },
    {
        "title": "Knog Oi Bell",
        "date": "Feb 9, 2021",
        "body": None,
        "body_html": (
            "<p>The <a href='https://www.knog.com/product/oi-classic-large/'>Knog Oi</a> bell's design is very slick in that it wraps around the bar.</p>"
            "<img src='https://www.bevilacqua.us/img/KnogOiBell-Black.jpg' alt='Knog Oi Bell'>"
            "<p>I've found new satisfaction in doing colorings to augment reading in the past year. I think I might even be getting better at it.</p>"
            "<img src='https://www.bevilacqua.us/img/PXL_20210120_221333330_sm.jpg' alt='Coloring'>"
            "<p>Adults are allowed to have fun with their food, too.</p>"
            "<img src='https://www.bevilacqua.us/img/PXL_20201211_142935273_sm.jpg' alt='Breakfast'>"
        ),
        "images": [],
    },
    {
        "title": "Site header design",
        "date": "Jan 31, 2021",
        "body_html": (
            "<p>Updated the site header. Anything bad I may have ever said about CSS, I take it all back.</p>"
            "<p>Also, I feel <a href='https://validator.w3.org/nu/?doc=https%3A%2F%2Fbevilacqua.us%2F'>validated</a>.</p>"
            "<p>Brushy Creek Park at the YMCA ridge bottom</p>"
            "<img src='https://www.bevilacqua.us/img/IMG_20200614_091057_sm.jpg' alt='Brushy Creek, TX'>"
        ),
        "images": [],
    },
    {
        "title": "Kitty Terminal",
        "date": "Jan 29, 2021",
        "body_html": (
            "<p>I've been meaning to mention the <a href='https://sw.kovidgoyal.net/kitty'>Kitty</a> terminal emulator for some time. "
            "Since installing it last October it has replaced Gnome Terminal and MacOS Terminal which I use daily. "
            "Performance, configuration, customization and documentation are impressive.</p>"
            "<p>Walnut Creek Park</p>"
            "<img src='https://www.bevilacqua.us/img/PANO_20200316_165535_sm.vr.jpg' alt='Walnut Creek Park'>"
        ),
        "images": [],
    },
    {
        "title": "Syntax Highlighting",
        "date": "Jan 29, 2021",
        "body_html": "<p>Updated site to utilize syntax highlighting with <a href='https://highlightjs.org'>Highlight.js</a>.</p>",
        "images": [],
    },
    {
        "title": "GoPro Hero8 as a webcam in Linux",
        "date": "Jan 27, 2021",
        "body": "After all of the time spent in Zoom/Webex during 2020, I found that I needed a new webcam for Linux. When I saw that it was possible to get this working in Unix I did some searching and pieced together the following. The great part about this is that the GoPro is the ultimate multi-tasker. I can use it on my MTB, in my car or as a webcam on my Linux workstation. Big win on this one.",
        "code_blocks": [
            {
                "lang": "bash",
                "code": r"""#!/bin/bash
  
echo
read -p "Plug in USB cable and turn on device. Press any key to continue.  " -n 1 -r
echo

iface=`ifconfig -a | grep enp | cut -f1 -d:`

echo
echo "inserting module v4l2loopback (/dev/video13)"
echo

modprobe v4l2loopback exclusive_caps=1 card_label="LinuxGoPro" video_nr=13

echo
echo "using interface: $iface"
echo

ip link set $iface up
ip address add 172.23.100.52/32 dev $iface
ip route add 172.23.100.0/24 dev $iface proto kernel scope link src 172.23.100.52

echo
echo "activating webcam @ 1080p"
echo

curl 172.23.100.51/gp/gpWebcam/START?res=1080

echo
echo " ffmpeg -threads 1 -i 'udp://@172.23.100.51:8554?overrun_nonfatal=1&fifo_size=50000000' -f:v mpegts -fflags nobuffer -vf format=yuv420p -f v4l2 /dev/video13 "
echo
echo " curl \"172.23.100.51/gp/gpWebcam/SETTINGS?fov=6\" "
echo""",
            },
            {
                "lang": "bash",
                "code": r"""#!/bin/bash

echo
echo deactivating webcam
echo

curl 172.23.100.51/gp/gpWebcam/STOP

iface=`ifconfig -a | grep enp | cut -f1 -d:`

echo
echo deconfiguring interface: $iface
echo

ip route del 172.23.100.0/24 dev $iface proto kernel scope link src 172.23.100.52
ip address del 172.23.100.52/32 dev $iface
ip link set $iface down

rmmod v4l2loopback""",
            },
        ],
        "images": [],
    },
    {
        "title": "Hello again, world",
        "date": "Jan 27, 2021",
        "body_html": (
            "<p>After many iterations of websites, I wanted something unbelievably simple to maintain due to time constraints. "
            "This is just a place for me to put ideas I'd like to share. This site's HTML/CSS layout modified from "
            "<a href='https://www.w3schools.com/howto/howto_css_blog_layout.asp'>W3Schools.com</a> blog example.</p>"
        ),
        "images": [],
    },
]

@app.route("/")
def index():
    return render_template("index.html", posts=POSTS)

@app.route("/get-ip")
def get_ip():
    # Returns the direct client IP address
    return {"ip": request.remote_addr}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
