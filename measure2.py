from PIL import ImageFont
D = "/usr/share/fonts/truetype/dejavu/"
b = lambda s: ImageFont.truetype(D + "DejaVuSans-Bold.ttf", s)
r = lambda s: ImageFont.truetype(D + "DejaVuSans.ttf", s)

lead = ["CLIMATE SUMMIT ENDS", "WITH NO DEAL AS FOSSIL", "FUEL FIGHT SINKS IT"]
print("lead 46/48", {s: round(max(b(s).getlength(t) for t in lead), 1) for s in (46, 48)})

print("lead body 23 halves")
lb = ["COP31 closes two days into overtime with no cover",
      "decision; the EU rejected the final text."]
for s in (25, 24, 23, 22):
    print(s, [round(r(s).getlength(t), 1) for t in lb])

print("grid heads split 34")
splits = [["DRONE KILLS NINE", "NEAR KYIV"], ["ASIA STOCKS SLIDE", "ON AI FEARS"],
          ["NINE SHOT AT", "A CONCERT"], ["FIGHTING STALLS", "EBOLA RESPONSE"]]
for s in (34, 32, 30):
    f = b(s)
    print(s, [[round(f.getlength(t), 1) for t in p] for p in splits])

print("grid bodies 2-line 21")
bs = [["186 drones launched overnight; Polish", "sites hold Kh-101 missile debris."],
      ["KOSPI -2.8% to a 10-month low;", "Anthropic falls 9% after its $81.3bn IPO."],
      ["One in critical condition; Delta's", "outage delays Thanksgiving flights."],
      ["11,613 cases and 5,678 deaths;", "South Sudan attack kills 24."]]
for s in (21, 20):
    f = r(s)
    print(s, [[round(f.getlength(t), 1) for t in p] for p in bs])

print("chips 20 vs 414 avail (minus 62 picto)")
for t in ["EUROPE  ·  KYIV REGION", "BUSINESS  ·  SEOUL", "AMERICAS  ·  CALIFORNIA", "AFRICA  ·  CONGO"]:
    print(t, round(b(20).getlength(t), 1))

print("hdr WORLD NEWS 26 spaced", round(b(26).getlength("W O R L D   N E W S"), 1))
print("date 78", round(b(78).getlength("23 NOVEMBER 2026"), 1))
print("lead chip 24", round(b(24).getlength("GLOBAL  ·  COP31, ANTALYA"), 1))
t = "Houthis hit Rabigh refinery · Hasina appeal stuck a year on · red fire ants found in Sydney"
for s in (22, 21, 20):
    print("also", s, round(r(s).getlength(t), 1), "label", round(b(s).getlength("ALSO TODAY   "), 1))
