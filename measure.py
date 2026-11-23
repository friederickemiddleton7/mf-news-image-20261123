from PIL import ImageFont
D = "/usr/share/fonts/truetype/dejavu/"
b = lambda s: ImageFont.truetype(D + "DejaVuSans-Bold.ttf", s)
r = lambda s: ImageFont.truetype(D + "DejaVuSans.ttf", s)

lead = ["CLIMATE SUMMIT ENDS", "WITH NO DEAL AS FOSSIL", "FUEL FIGHT SINKS IT"]
print("lead headline")
for sz in (54, 52, 50, 48, 46, 44):
    f = b(sz)
    print(sz, [round(f.getlength(t), 1) for t in lead])

print("lead body")
body = "COP31 closes two days into overtime with no cover decision; the EU rejected the final text."
for sz in (25, 24, 23, 22):
    print(sz, round(r(sz).getlength(body), 1))

print("grid heads")
gh = ["DRONE KILLS NINE NEAR KYIV", "ASIA STOCKS SLIDE ON AI FEARS",
      "NINE SHOT AT A CONCERT", "FIGHTING STALLS EBOLA RESPONSE"]
for sz in (34, 32, 30):
    f = b(sz)
    print(sz, [round(f.getlength(t), 1) for t in gh])

print("grid bodies")
gb = ["186 drones launched overnight; Polish sites hold Kh-101 missile debris.",
      "KOSPI -2.8% to a 10-month low; Anthropic falls 9% after its $81.3bn IPO.",
      "One in critical condition; Delta's outage delays Thanksgiving flights.",
      "11,613 cases and 5,678 deaths; South Sudan attack kills 24."]
for sz in (21, 20):
    print(sz, [round(r(sz).getlength(t), 1) for t in gb])

print("chips 20", [round(b(20).getlength(t), 1) for t in
                   ["EUROPE  ·  KYIV REGION", "BUSINESS  ·  SEOUL",
                    "AMERICAS  ·  CALIFORNIA", "AFRICA  ·  CONGO"]])
print("chips 18", [round(b(18).getlength(t), 1) for t in
                   ["EUROPE  ·  KYIV REGION", "BUSINESS  ·  SEOUL",
                    "AMERICAS  ·  CALIFORNIA", "AFRICA  ·  CONGO"]])
print("lead chip 24", round(b(24).getlength("GLOBAL  ·  COP31, ANTALYA"), 1))
print("date 78", round(b(78).getlength("23 NOVEMBER 2026"), 1))
print("date 84", round(b(84).getlength("23 NOVEMBER 2026"), 1))
t = "Houthis hit Rabigh refinery · Hasina appeal stuck a year on · red fire ants found in Sydney"
for sz in (22, 21, 20):
    print("also", sz, round(r(sz).getlength(t), 1))
print("also label", round(b(22).getlength("ALSO TODAY   "), 1))
