import datetime, sys

POOLS = {
 "Power Tools": ["Oscillating Multi-Tool","Cordless Jigsaw","Cordless Circular Saw","Benchtop Drill Press","Cordless Impact Wrench","Cordless Heat Gun","Cordless Caulking Gun","Random Orbit Polisher","Cordless Detail Sander","Rotary Tool Kit","Cordless Cut-Off Tool","Biscuit Joiner","Cordless Planer","Benchtop Belt Sander","Cordless Brad Nailer","Cordless Finish Nailer","Cordless Framing Nailer","Cordless Oscillating Tool","Cordless Router","Cordless Jobsite Radio"],
 "Hand Tools": ["Flaring Tool Kit","Pipe Bending Spring Set","Tubing Cutter","Electrician's Pliers Set","Lineman's Pliers","Offset Screwdriver Set","Gunsmith Screwdriver Set","Magnetic Wristband Tool Holder","Foldable Hex Key Set","Ratcheting Wrench Set","Needle Nose Pliers Set","Locking Pliers Set","Pipe Wrench Set","Combination Wrench Set","Dead Blow Mallet","Japanese Chisels","Block Plane","Shoulder Plane","Card Scraper","Wood Rasp","Marking Knife","Marking Gauge","Mortise Gauge","Dovetail Gauge","Coping Saw","Japanese Pull Saw","Dovetail Saw","Flush Cut Saw"],
 "Outdoor Power Equipment": ["Cordless Leaf Blowers","Walk-Behind Brush Cutters","Electric Snow Blowers","Cordless Pole Saws","Cordless Lawn Mowers","Cordless Lawn Edger","Cordless Hedge Trimmer","Cordless Grass Shears","Electric Log Splitters","Weed Torches","Cordless String Trimmer","Mini Cultivators","Garden Tillers","Electric Chainsaw","Cordless Leaf Vacuum"],
 "Measuring Tools": ["Digital Angle Finder","Stud Finder Wall Scanner","Digital Protractor","Self-Leveling Cross Line Laser","Pin-Type Moisture Meter","Pinless Moisture Meter","Wire Tracer Kit","Digital Multimeter for Beginners","Clamp Meter","Magnetic Angle Gauge","Pipe Laser Level","Bluetooth Laser Measure","Ultrasonic Distance Meter","Digital Caliper","Torpedo Level Set","Combination Square","Speed Square","Sliding T-Bevel","Marking Gauge","Dovetail Marker"],
 "Home Improvement / Woodworking": ["Pocket Hole Jig","Dovetail Jig","Mortise Jig","Doweling Jig","Circle Cutting Jig","Crosscut Sled","Benchtop Router Table","Wood Lathe","Drum Sander","Scroll Saw","Tile Leveling System","Grout Float Set","Drywall Screw Gun","PEX Pipe Crimping Tool","Caulk Finishing Tool Set","Corner Bead Crimper","Benchtop Band Saw","Random Orbit Sander","Oscillating Spindle Sander","Knee Pads for Flooring"],
 "Lawn & Garden": ["Drip Irrigation Kits","Soaker Hose Systems","Garden Hose Reel Carts","Soil Moisture Meters","pH Meters for Soil","Seed Spreaders","Broadfork Garden Tools","Stirrup Hoe","Bulb Planters","Garden Kneeler Seat","Compost Tumbler","Rain Gauge","Garden Hose Nozzle Set","Potting Bench","Lawn Aerator Shoes","Garden Tool Set","Raised Garden Bed Kit","Cold Frame Greenhouse"],
}
COUNTS = {"Power Tools":2,"Hand Tools":2,"Outdoor Power Equipment":2,"Measuring Tools":1,"Home Improvement / Woodworking":2,"Lawn & Garden":1}
MODIFIERS = ["cordless","corded","battery-powered","for beginners","for professionals","heavy duty","compact","mini","benchtop","under $50","under $100","under $200","for woodworking","for cabinet making","for trim work","for rough carpentry","with dust collection","Japanese-style","precision","self-centering","magnetic","telescoping"]

def pick(date_str):
    d = datetime.date.fromisoformat(date_str)
    ordinal = d.toordinal()
    rows = []
    for c, (cat, pool) in enumerate(POOLS.items()):
        k = COUNTS[cat]
        L = len(pool)
        for i in range(k):
            item_idx = (ordinal + c*17 + i*(L//2 + 3)) % L
            mod_idx = (ordinal*3 + c*11 + i*7 + 5) % len(MODIFIERS)
            rows.append((cat, pool[item_idx], MODIFIERS[mod_idx]))
    return rows

for ds in sys.argv[1:]:
    print(f"--- {ds} ---")
    for cat, item, mod in pick(ds):
        print(f"  [{cat}] {item} ({mod})")
