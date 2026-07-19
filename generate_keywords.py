import datetime, sys

# Pools organized as {category: {modifier_group: [product types]}} so every
# product only ever pairs with modifiers that make sense for it.
# Exact top-performing/published keywords are deliberately excluded.
POOLS = {
 "Power Tools": {
  "pw": ["Track Saw","Plunge Router","Fixed Base Router","Trim Router","Cordless Router","Cordless Jigsaw","Cordless Circular Saw","Cordless Planer","Cordless Miter Saw","Sliding Compound Miter Saw","Cordless Reciprocating Saw","Detail Mouse Sander","Cordless Detail Sander","Biscuit Joiner","Pin Nailer","Cordless Finish Nailer","Cordless Framing Nailer","Flooring Nailer","Electric Staple Gun","Oscillating Multi-Tool","Cordless Oscillating Tool","HVLP Paint Sprayer","Cordless Paint Sprayer","Rotary Tool Kit","Engraving Tool","Electric Glue Gun","Cordless Heat Gun","Cordless Caulking Gun","Cordless Work Light","Cordless Jobsite Radio"],
  "bench": ["Benchtop Drill Press","Floor Standing Drill Press","Benchtop Belt Sander","Benchtop Disc Sander","Combination Belt Disc Sander","Jobsite Table Saw","Tile Wet Saw","Variable Speed Bench Grinder","Cordless Table Saw"],
  "pmm": ["Angle Grinder","Cordless Angle Grinder","Die Grinder","Metal Chop Saw","Cold Cut Metal Saw","Electric Metal Shears","Metal Nibbler Tool","MIG Welder","Stick Welder","Flux Core Welder","Plasma Cutter","Cordless Cut-Off Tool"],
  "pmd": ["Rotary Hammer Drill","Demolition Hammer","Cordless Rotary Hammer","Right Angle Drill","Magnetic Drill Press","Cordless Impact Wrench","Cordless Impact Driver","Cordless Hammer Drill","Roofing Nailer","Siding Nailer","Palm Nailer","Random Orbit Polisher","Car Buffer Polisher","Air Ratchet","Air Impact Wrench","Air Die Grinder","Pancake Air Compressor","Quiet Air Compressor","Airless Paint Sprayer"],
 },
 "Hand Tools": {
  "hw": ["Japanese Chisels","Bench Chisel Set","Mortise Chisel Set","Wood Carving Chisel Set","Carving Gouge Set","Wooden Joiners Mallet","Block Plane","Shoulder Plane","Jack Plane","Jointer Plane","Router Plane","Rabbet Plane","Scrub Plane","Spokeshave","Drawknife","Card Scraper","Cabinet Scraper Set","Scraper Burnisher","Honing Guide","Whetstone Sharpening Kit","Diamond Sharpening Plate","Leather Strop Kit","Wood Rasp","Rasp File Set","Riffler File Set","Marking Knife","Marking Gauge","Mortise Gauge","Dovetail Gauge","Coping Saw","Japanese Pull Saw","Dovetail Saw","Flush Cut Saw","Tenon Saw","Veneer Saw","Bar Clamp Set","Parallel Clamp Set","Pipe Clamp Set","Toggle Clamp Set","Band Clamp","Corner Clamp Set","Spring Clamp Set","Woodworking Vise","Dead Blow Mallet"],
  "hm": ["Ratcheting Wrench Set","Combination Wrench Set","Adjustable Wrench Set","Strap Wrench Set","Crowfoot Wrench Set","Flare Nut Wrench Set","Impact Socket Set","Deep Socket Set","Pass Through Socket Set","Stubby Wrench Set","Needle Nose Pliers Set","Locking Pliers Set","Snap Ring Pliers Set","Tongue and Groove Pliers","End Cutting Pliers","Hose Clamp Pliers","Precision Screwdriver Set","Torx Screwdriver Set","Impact Screwdriver Set","Offset Screwdriver Set","Gunsmith Screwdriver Set","Foldable Hex Key Set","Magnetic Wristband Tool Holder","Claw Hammer","Framing Hammer","Ball Peen Hammer","Drilling Hammer","Trim Hammer","Pry Bar Set","Cat's Paw Nail Puller","Utility Knife Set","Aviation Snips Set","Tap and Die Set","Thread Repair Kit","Deburring Tool Kit","Bench Vise","Machinist Vise","Hand Riveter","Rivet Nut Tool","Punch and Chisel Set","Transfer Punch Set","Nail Set Kit","Scratch Awl","Screw Extractor Set","Bolt Cutters","Hacksaw Frame","Keyhole Saw","Bow Saw"],
  "he": ["Electrician's Pliers Set","Lineman's Pliers","Insulated Screwdriver Set","Wire Stripper Crimper","Cable Cutters","Fish Tape Reel","Conduit Bender","Fencing Pliers"],
  "hp": ["Flaring Tool Kit","Pipe Bending Spring Set","Tubing Cutter","Pipe Wrench Set","Basin Wrench"],
 },
 "Outdoor Power Equipment": {
  "og": ["Backpack Leaf Blower","Cordless Backpack Blower","Walk-Behind Leaf Blower","Cordless Leaf Vacuum","Leaf Mulcher Shredder","Lawn Dethatcher","Electric Dethatcher Scarifier","Plug Aerator","Overseeder","Robot Lawn Mower","Two-Stage Snow Blower","Cordless Snow Blower","Electric Power Snow Shovel","Electric Snow Blowers","Earth Auger","Stump Grinder","Wood Chipper","Chipper Shredder","Telescoping Hedge Trimmer","Pole Hedge Trimmer","Cordless Hedge Trimmer","Cordless Grass Shears","Walk-Behind Brush Cutters","Cordless Pole Saws","Top Handle Chainsaw","Mini Chainsaw","Cordless Chainsaw","Cordless Lawn Edger","Cordless String Trimmer","Wheeled String Trimmer","Electric Log Splitters","Kinetic Log Splitter","Backpack Sprayer","Battery Powered Backpack Sprayer","Mini Cultivators","Garden Tillers","Rear Tine Tiller","Cordless Leaf Blowers","Electric Wheelbarrow","Cordless Earth Auger","Electric Garden Shredder","Battery Powered Weed Sprayer"],
  "ogm": ["Manual Log Splitter","Post Hole Digger","Weed Torches","String Trimmer Head","Electric Chainsaw Sharpener","Lawn Roller","Tow-Behind Aerator","Lawn Sweeper","Salt Spreader"],
 },
 "Measuring Tools": {
  "mw": ["Digital Angle Finder","Stud Finder Wall Scanner","Digital Protractor","Pin-Type Moisture Meter","Pinless Moisture Meter","Digital Caliper","Contour Gauge","Combination Square","Speed Square","Framing Square","Drywall T-Square","Center Finder Tool","Sliding T-Bevel","Dovetail Marker","Torpedo Level Set","Box Beam Level","Digital Level","Post Level","Chalk Line Reel","Plumb Bob Kit"],
  "me": ["Wire Tracer Kit","Digital Multimeter","Clamp Meter","Non-Contact Voltage Tester","Outlet Circuit Tester","Circuit Breaker Finder","Thermal Imaging Camera","Infrared Thermometer","Gas Leak Detector","Sound Level Meter","Light Meter","Anemometer"],
  "mm": ["Micrometer Set","Dial Indicator Set","Magnetic Base Indicator Holder","Feeler Gauge Set","Depth Gauge","Height Gauge","Thread Pitch Gauge","Machinist Square Set","Magnetic Angle Gauge"],
  "mg": ["Self-Leveling Cross Line Laser","Rotary Laser Level","Green Beam Laser Level","3-Plane Laser Level","Pipe Laser Level","Bluetooth Laser Measure","Ultrasonic Distance Meter","Inspection Camera Borescope","Line Level Set","Water Level Kit"],
 },
 "Home Improvement / Woodworking": {
  "jig": ["Pocket Hole Jig","Dovetail Jig","Mortise Jig","Doweling Jig","Circle Cutting Jig","Crosscut Sled","Box Joint Jig","Taper Jig","Spline Jig","Shelf Pin Jig","Cabinet Hardware Jig","Concealed Hinge Jig","Door Hinge Jig","Drawer Slide Jig","Router Sled Flattening Mill","Dado Jig","Track Saw Guide Rail","Circular Saw Guide Track","Portable Drill Guide","Router Bit Set","Forstner Bit Set","Drill Bit Sharpener","Featherboard Set","Push Block Set","Bench Dog Set","Moxon Vise Kit","Router Table Fence","Router Lift","Wood Lathe Chisel Set"],
  "bench2": ["Benchtop Router Table","Wood Lathe","Midi Wood Lathe","Drum Sander","Scroll Saw","Benchtop Band Saw","Oscillating Spindle Sander","Random Orbit Sander","Benchtop Jointer","Benchtop Planer","Portable Workbench","Clamping Workbench","Folding Sawhorse Set"],
  "reno": ["Tile Leveling System","Manual Tile Cutter","Tile Nipper","Grout Removal Tool","Grout Float Set","Tile Drill Bit Set","Drywall Screw Gun","Drywall Lift","Drywall Cutout Router","Mud Mixer Drill","Drywall Taping Tool Set","Corner Bead Crimper","PEX Pipe Crimping Tool","PEX Expander Tool","Pipe Threader Kit","Caulk Finishing Tool Set","Laminate Flooring Cutter","Floor Scraper","Flooring Knee Pads","Paint Edger Kit","Paint Mixer Drill Attachment"],
 },
 "Lawn & Garden": {
  "gg": ["Broadfork Garden Tools","Stirrup Hoe","Bulb Planters","Garden Kneeler Seat","Pruning Shears","Bypass Loppers","Anvil Loppers","Hedge Shears","Grafting Tool Kit","Hori Hori Knife","Garden Trowel Set","Hand Cultivator","Digging Fork","Mattock Pick","Garden Tool Set","Wheelbarrow","Garden Dump Cart","Leaf Collection Tarp","Garden Sieve","Fruit Picker Pole","Firewood Rack","Lawn Aerator Shoes","Seed Spreaders"],
  "gw": ["Drip Irrigation Kits","Soaker Hose Systems","Garden Hose Reel Carts","Garden Hose Nozzle Set","Watering Wand","Hose Timer","Hose Splitter","Watering Can Set","Rain Barrel Kit","Rain Gauge","Soil Moisture Meters","Soil pH Meter","Soil Test Kit"],
  "gs": ["Compost Tumbler","Worm Composting Bin","Compost Thermometer","Compost Aerator Tool","Potting Bench","Raised Garden Bed Kit","Cold Frame Greenhouse","Greenhouse Kit","Seed Starting Tray Kit","Seedling Heat Mat","Seedling Grow Light","Tomato Cages","Trellis Netting","Plant Support Stakes","Landscape Fabric"],
 },
}

MODGROUPS = {
 "pw":    ["cordless","brushless","compact","for beginners","for woodworking","for cabinet making","for trim work","under $100","under $200","for small shops","variable speed"],
 "bench": ["benchtop","for beginners","for small shops","for woodworking","with dust collection","under $200","variable speed","for hobbyists","for home workshops"],
 "pmm":   ["cordless","heavy duty","for beginners","for metalworking","for welding projects","under $100","under $200","compact"],
 "pmd":   ["cordless","brushless","heavy duty","for beginners","for home garage","for automotive work","under $100","under $200","compact"],
 "hw":    ["for beginners","for fine woodworking","for cabinet making","for dovetail joinery","precision","for hardwood","for furniture making","under $50","under $100"],
 "hm":    ["for mechanics","for automotive work","heavy duty","for beginners","for professionals","for home garage","under $50","under $100","compact"],
 "he":    ["for electricians","for home wiring","heavy duty","for professionals","for beginners","under $50"],
 "hp":    ["for plumbing","for tight spaces","for copper tubing","heavy duty","for beginners","under $50"],
 "og":    ["battery-powered","for small yards","for large properties","heavy duty","lightweight","for homeowners","under $200","for tough jobs","quiet","for hilly terrain","commercial grade","under $300","for spring cleanup","for fall cleanup"],
 "ogm":   ["heavy duty","for beginners","for homeowners","under $100","compact","for firewood prep","for large properties","budget-friendly","for small yards","long-lasting"],
 "mw":    ["for woodworking","for cabinet installation","precision","for beginners","digital","for framing","high accuracy","under $50"],
 "me":    ["for electricians","for beginners","for home use","for HVAC work","for automotive diagnostics","under $50","under $100"],
 "mm":    ["for machinists","high accuracy","for metalworking","digital","for beginners","under $50","under $100"],
 "mg":    ["for home renovation","for construction","for beginners","high accuracy","for tile work","for framing","under $100","under $200"],
 "jig":   ["for beginners","for cabinet making","for furniture making","precision","for hardwood","for plywood","under $50","under $100","adjustable","for thick boards","compact","heavy duty"],
 "bench2":["for beginners","for small shops","for hobbyists","with dust collection","for hardwood","under $200","compact","for home workshops","space-saving","for garage shops","quiet"],
 "reno":  ["for beginners","for professionals","for DIY renovation","heavy duty","for bathroom remodel","under $100","professional grade","for kitchen remodel","for basement finishing"],
 "gg":    ["for raised beds","for small gardens","for vegetable gardens","for seniors","for beginners","heavy duty","under $50","ergonomic"],
 "gw":    ["for raised beds","for small gardens","for large gardens","for vegetable gardens","under $50","heavy duty","for greenhouses"],
 "gs":    ["for small backyards","for beginners","for vegetable gardens","under $100","heavy duty","for cold climates"],
}

COUNTS = {"Power Tools":2,"Hand Tools":2,"Outdoor Power Equipment":2,"Measuring Tools":1,"Home Improvement / Woodworking":2,"Lawn & Garden":1}

def phrase(item, mod):
    if mod.split()[0] in ("for","under","with"):
        return f"{item.lower()} {mod}"
    return f"{mod} {item.lower()}"

def _combos(groups):
    out = []
    for g, items in groups.items():
        for item in items:
            for mod in MODGROUPS[g]:
                if mod.split()[0].lower() not in item.lower():
                    out.append((item, mod))
    return out

def _coprime_step(T):
    from math import gcd
    s = max(2, int(T * 0.618))
    while gcd(s, T) != 1:
        s += 1
    return s

def pick(date_str):
    d = datetime.date.fromisoformat(date_str)
    n = d.toordinal()
    rows = []
    for c, (cat, groups) in enumerate(POOLS.items()):
        combos = _combos(groups)
        T = len(combos)
        step = _coprime_step(T)
        for i in range(COUNTS[cat]):
            s = n * COUNTS[cat] + i
            item, mod = combos[(s * step + c * 101) % T]
            rows.append((cat, phrase(item, mod)))
    return rows

if __name__ == "__main__":
    for ds in sys.argv[1:]:
        print(f"--- {ds} ---")
        for cat, kw in pick(ds):
            print(f"  [{cat}] {kw}")
