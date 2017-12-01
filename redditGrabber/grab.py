from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys

# Parse args, make sure we have a subreddit
if len(sys.argv) < 3:
    print("Usage: python3 {} subredditName numLinks".format(sys.argv[0]));
    exit();

# Create webdriver
driver = webdriver.Firefox()

# Fetch starting webpage
driver.get("http://www.reddit.com/r/"+sys.argv[1])
desiredLinks = int(sys.argv[2]);

time.sleep(2);

# Investigate page structure (manual)
# source = driver.page_source
# soup = BeautifulSoup(source, 'html.parser')
# print(soup.prettify());

# Find "Top" button
# <ul class="tabmenu ">
# <li>
# <a class="choice" href="https://www.reddit.com/r/AMA/top/">
# top
# </a>
# </li>

tabMenuItem = driver.find_element_by_class_name("tabmenu");
topButton = tabMenuItem.find_element_by_link_text('top')
# print("\n\n\n");
# print(tabMenuItem.get_attribute('innerHTML'));
# print("\n\n\n");
# print(topButton.get_attribute('innerHTML'));
topButton.click();

time.sleep(2)

# source = driver.page_source
# soup = BeautifulSoup(source, 'html.parser')
# print("\n\n\n\n\n\n\n\n\n\n");
# print(soup.prettify());

time.sleep(1);

dropDownMenu = driver.find_element_by_xpath("//div[contains(@class,'menuarea')]//div[contains(@class,'dropdown')]");
dropDownMenu.click();
time.sleep(1);

allTimeButton = driver.find_element_by_xpath("//div[contains(@class,'menuarea')]//a[contains(text(),'all time')]");
allTimeButton.click();
time.sleep(1);

 # <div class="menuarea">
 #    <div class="spacer">
 #     <span class="dropdown-title lightdrop">
 #      links from:
 #     </span>
 #     <div class="dropdown lightdrop" onclick="open_menu(this)">
 #      <span class="selected">
 #       past 24 hours
 #      </span>
 #     </div>
 #     <div class="drop-choices lightdrop">
 #      <form action="https://www.reddit.com/r/AMA/top/" method="POST">
 #       <input name="t" type="hidden" value="hour">
 #        <a class="choice" href="https://www.reddit.com/r/AMA/top/" onclick="$(this).parent().submit(); return false;">
 #         past hour
 #        </a>
 #       </input>
 #      </form>
 #      <form action="https://www.reddit.com/r/AMA/top/" method="POST">
 #       <input name="t" type="hidden" value="week">
 #        <a class="choice" href="https://www.reddit.com/r/AMA/top/" onclick="$(this).parent().submit(); return false;">
 #         past week
 #        </a>
 #       </input>
 #      </form>
 #      <form action="https://www.reddit.com/r/AMA/top/" method="POST">
 #       <input name="t" type="hidden" value="month">
 #        <a class="choice" href="https://www.reddit.com/r/AMA/top/" onclick="$(this).parent().submit(); return false;">
 #         past month
 #        </a>
 #       </input>
 #      </form>
 #      <form action="https://www.reddit.com/r/AMA/top/" method="POST">
 #       <input name="t" type="hidden" value="year">
 #        <a class="choice" href="https://www.reddit.com/r/AMA/top/" onclick="$(this).parent().submit(); return false;">
 #         past year
 #        </a>
 #       </input>
 #      </form>
 #      <form action="https://www.reddit.com/r/AMA/top/" method="POST">
 #       <input name="t" type="hidden" value="all">
 #        <a class="choice" href="https://www.reddit.com/r/AMA/top/" onclick="$(this).parent().submit(); return false;">
 #         all time
 #        </a>
 #       </input>
 #      </form>
 #     </div>

linksRetreived = 0;
### Next, we need to fetch all the posts on the page
while linksRetreived < desiredLinks:
    links = driver.find_elements_by_xpath("//div[contains(@class,'sitetable')]/div[contains(@class,'thing')]");

    print("This page has {} links".format(len(links)));

    for link in links:
        print("------------------------");
        #print(link.get_attribute("outerHTML"));
        title = link.find_element_by_xpath(".//a[contains(@class,'title')]").text;
        print("#{} - {}".format(link.get_attribute("data-rank"),title));
        print("{} comments, {} score".format(link.get_attribute("data-comments-count"),link.get_attribute("data-score")));
        print("Url {}".format(link.get_attribute("data-url")));
        print("\n");

        linksRetreived += 1;

    time.sleep(4);

    # Step to the next page
    nextButton = driver.find_element_by_xpath("//span[contains(@class,'next-button')]");
    nextButton.click();
    time.sleep(3);


#Parent:
#<div class="sitetable linklisting" id="siteTable">

# <div class=" thing id-t3_1ol60b odd link self" data-author="steveberke" data-author-fullname="t2_4g68v" data-comments-count="104" data-context="listing" data-domain="self.AMA" data-fullname="t3_1ol60b" data-num-crossposts="0" data-permalink="/r/AMA/comments/1ol60b/im_currently_running_for_mayor_of_miami_beach/" data-rank="38" data-score="547" data-subreddit="AMA" data-subreddit-fullname="t5_2r4eo" data-timestamp="1381947484000" data-type="link" data-url="/r/AMA/comments/1ol60b/im_currently_running_for_mayor_of_miami_beach/" data-whitelist-status="all_ads" id="thing_t3_1ol60b" onclick="click_thing(this)">
#       <p class="parent">
#       </p>
#       <span class="rank">
#        38
#       </span>
#       <div class="midcol unvoted">
#        <div aria-label="upvote" class="arrow up login-required archived access-required" data-event-action="upvote" role="button" tabindex="0">
#        </div>
#        <div class="score dislikes" title="546">
#         546
#        </div>
#        <div class="score unvoted" title="547">
#         547
#        </div>
#        <div class="score likes" title="548">
#         548
#        </div>
#        <div aria-label="downvote" class="arrow down login-required archived access-required" data-event-action="downvote" role="button" tabindex="0">
#        </div>
#       </div>
#       <div class="entry unvoted">
#        <div class="top-matter">
#         <p class="title">
#          <a class="title may-blank " data-event-action="title" data-href-url="/r/AMA/comments/1ol60b/im_currently_running_for_mayor_of_miami_beach/" data-inbound-url="/r/AMA/comments/1ol60b/im_currently_running_for_mayor_of_miami_beach/?utm_content=title&amp;utm_medium=browse&amp;utm_source=reddit&amp;utm_name=AMA" href="/r/AMA/comments/1ol60b/im_currently_running_for_mayor_of_miami_beach/" rel="" tabindex="1">
#           I'm currently running for Mayor of Miami Beach against a near billionaire and a career politician and I'm making a documentary about the dirty political process.
#          </a>
#          <span class="domain">
#           (
#           <a href="/r/AMA/">
#            self.AMA
#           </a>
#           )
#          </span>
#         </p>
#         <div class="expando-button collapsed hide-when-pinned selftext">
#         </div>
#         <p class="tagline ">
#          submitted
#          <time class="" datetime="2013-10-16T18:18:04+00:00" title="Wed Oct 16 18:18:04 2013 UTC">
#           4 years ago
#          </time>
#          <time class="edited-timestamp" datetime="2013-10-16T19:37:56+00:00" title="last edited 4 years ago">
#           *
#          </time>
#          by
#          <a class="author may-blank id-t2_4g68v" href="https://www.reddit.com/user/steveberke">
#           steveberke
#          </a>
#          <span class="userattrs">
#          </span>
#         </p>
#         <ul class="flat-list buttons">
#          <li class="first">
#           <a class="bylink comments may-blank" data-event-action="comments" data-href-url="/r/AMA/comments/1ol60b/im_currently_running_for_mayor_of_miami_beach/" data-inbound-url="/r/AMA/comments/1ol60b/im_currently_running_for_mayor_of_miami_beach/?utm_content=comments&amp;utm_medium=browse&amp;utm_source=reddit&amp;utm_name=AMA" href="https://www.reddit.com/r/AMA/comments/1ol60b/im_currently_running_for_mayor_of_miami_beach/" rel="nofollow">
#            104 comments
#           </a>
#          </li>
#          <li class="share">
#           <a class="post-sharing-button" href="javascript: void 0;">
#            share
#           </a>
#          </li>
#          <li class="link-save-button save-button login-required">
#           <a href="#">
#            save
#           </a>
#          </li>
#          <li>
#           <form action="/post/hide" class="state-button hide-button" method="post">
#            <input name="executed" type="hidden" value="hidden">
#             <span>
#              <a class=" " data-event-action="hide" href="javascript:void(0)" onclick="change_state(this, 'hide', hide_thing);">
#               hide
#              </a>
#             </span>
#            </input>
#           </form>
#          </li>
#          <li class="report-button login-required">
#           <a class="reportbtn access-required" data-event-action="report" href="javascript:void(0)">
#            report
#           </a>
#          </li>
#         </ul>
#         <div class="reportform report-t3_1ol60b">
#         </div>
#        </div>
#        <div class="expando expando-uninitialized" data-pin-condition="function() {return this.style.display != 'none';}" style="display: none">
#         <span class="error">
#          loading...
#         </span>
#        </div>
#       </div>
#       <div class="child">
#       </div>
#       <div class="clearleft">
#       </div>
#      </div>
#      <div class="clearleft">
#      </div>

# <form action="https://www.reddit.com/r/worldnews/post/login" class="login-form login-form-side" id="login_login-main" method="post">
#      <input name="op" type="hidden" value="login-main">
#       <input maxlength="20" name="user" placeholder="username" tabindex="1" type="text">
#        <input name="passwd" placeholder="password" tabindex="1" type="password">
#         <div class="g-recaptcha" data-sitekey="6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC">
#         </div>
#         <div class="status">
#         </div>
#         <div id="remember-me">
#          <input id="rem-login-main" name="rem" tabindex="1" type="checkbox">
#           <label for="rem-login-main">
#            remember me
#           </label>
#           <a class="recover-password" href="/password">
#            reset password
#           </a>
#          </input>
#         </div>
#         <div class="submit">
#          <span class="throbber">
#          </span>
#          <button class="btn" tabindex="1" type="submit">
#           login
#          </button>
#         </div>
#         <div class="clear">
#         </div>
#        </input>
#       </input>
#      </input>
#     </form>
### Insert username and password

exit()

userField = driver.find_element_by_xpath("//form[contains(@class,'login-form')]//input[@name='user']");
passField = driver.find_element_by_xpath("//form[contains(@class,'login-form')]//input[@name='passwd']");
submitButton = driver.find_element_by_xpath("//form[contains(@class,'login-form')]//button[@type='submit']");

userField.send_keys("UserName");
time.sleep(2);
passField.send_keys("MyPass");
time.sleep(5);

submitButton.click();
