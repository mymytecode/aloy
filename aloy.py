from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        lcp = float(request.form["lcp"])
        ttfb = float(request.form["ttfb"])
        lcp_start_loading_time = float(request.form["lcp_start_loading_time"])
        resource_load_time = float(request.form["resource_load_time"])

        recommandations = evaluer_conditions(lcp, ttfb, lcp_start_loading_time, resource_load_time)
        recommandations_html = "<br><br>".join(recommandations)

        return render_template("index.html", lcp=lcp, ttfb=ttfb, lcp_start_loading_time=lcp_start_loading_time, resource_load_time=resource_load_time, recommandations_html=recommandations_html)

    return render_template('index.html')

def evaluer_conditions(lcp, ttfb, lcp_start_loading_time, resource_load_time):
    recommandations = []

    resource_load_delay = lcp_start_loading_time - ttfb
    element_render_delay = lcp - (resource_load_time + lcp_start_loading_time)

    if lcp > 2500:
        recommandations.append("The element that embodies the LCP on this page is slow to render.")
        recommandations.append("How to optimize the LCP?")

    if ttfb > 0.4 * lcp:
        recommandations.append("Investigate why your Time To First Byte is high.")
        recommandations.append("The first useful byte is only available after {} ms.".format(int(ttfb)))

        ttfb_recommendations = [
            "Nothing can happen on the frontend until the backend delivers that first byte of content, so anything you can do to speed up your TTFB will improve every other load metric as well.",
            "How to improve TTFB? Avoid multiple page redirects; Limit the traffic coming from abroad if there is any or rely on a CDN present in all the concerned geographies. If Connection Time is high, work with security experts to improve the security certificate. If it is the Waiting Time that is high, then it is necessary to work on the caching of the contents."
        ]
        recommandations.extend(ttfb_recommendations)

    if resource_load_delay > 0.1 * lcp:
        recommandations.append("Eliminate unnecessary resource load delay: Even when the LCP element is fetched, the browser doesn’t show it. It renders after {} ms.".format(int(resource_load_delay)))
        recommandations.append("The LCP element is not immediately loaded once the page is available. It starts loading after Resource load delay.")
        recommandations.append("To eliminate unnecessary resource load delay, your LCP resource should always be discoverable from the HTML source. In cases where the resource is only referenced from an external CSS or JavaScript file, then the LCP resource should be preloaded, with a high fetch priority.")

    if resource_load_time > 0.4 * lcp:
        recommandations.append("Reduce resource load time")

        resource_load_time_recommendations = [
            "The LCP element is very fast to load",
            "Reduce the size of the resource (Serve the optimal image size, use modern image format, compress images, reduce web font size). Reduce the distance the resource has to travel. Reduce contention for network bandwidth. Eliminate the network time entirely."
        ]
        recommandations.extend(resource_load_time_recommendations)

    if element_render_delay > 0.1 * lcp:
        recommandations.append("Eliminate element render delay: Even when the LCP element is fetched, the browser doesn’t show it. It renders after {} ms.".format(int(element_render_delay)))
        recommandations.append("The LCP element is maybe waiting for some JavaScript code to load. => Minify scripts and/or defer non-critical scripts. The main thread is maybe blocked due to long tasks, and rendering work needs to wait until those long tasks complete.")

    return recommandations


if __name__ == "__main__":
  app.run(debug=True)

