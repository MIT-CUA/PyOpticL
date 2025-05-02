from PyOpticL import layout, optomech
from datetime import datetime

name = "Doublepass"
date_time = datetime.now().strftime("%m/%d/%Y")
label = name + " " +  date_time

base_dx = 11*layout.inch + 2*layout.inch - 0.25*layout.inch
base_dy = 5.75*layout.inch
base_dz = 15/16*layout.inch
gap = 0

x_offset = 0.25
y_offset = 0.8/25.4+39/25.4

mount_holes_temp = [(1,0), (11,0), (9,2)]

mount_holes = []
for x,y in mount_holes_temp:
    mount_holes.append((x+x_offset, y+y_offset))


# Note that for mirror_mount_c05g, an offset of 6mm is needed as the pos is 
# centered at the optical start, not the drill hole as in openscad. 

d_inch = 25.4

mount_hole_xoff = 13
mount_hole_yoff = 92-3*d_inch

x_tri = 24
aom_axis = 38 # distance to second optical axis
pbs_axis = aom_axis + 38
aom_xpos = 223

# input optics
module_output_offset = 19.1 + 15
mIn1_xpos = module_output_offset
mIn1_ypos = 78
mIn2_ypos = base_dy - 25
mIn2_xpos = mIn1_xpos + 1.8 * d_inch
mIn3_xpos = mIn2_xpos
fb_xpos = mIn1_xpos
fb_ypos = base_dy

# pbs and fiber out
pbs_xpos = mIn3_xpos + 75
mOut1_xpos = pbs_xpos
mOut1_ypos = pbs_axis + 47
hwp_xpos = mOut1_xpos + 35
hwp_ypos = mOut1_ypos
mOut2_xpos = base_dx - module_output_offset-2*layout.inch
fb_out_xpos = mOut2_xpos
fb_out_ypos = base_dy

# turning mirrors
m1_xpos = 262

# telescope
tele1 = True # 1/2
fiber = False # no telescope
pccIn_xpos = aom_xpos + 20

# cat's eye components
left_axis = 60
qwp_xpos = aom_xpos - 60
pcx1_xpos = aom_xpos - 100 # 100mm focal distance lens
pcx1a_xpos = pcx1_xpos - 15
mCat_xpos = pcx1_xpos - 100 - 1

fpout2_xpos = fb_out_xpos + d_inch + 6

# testing
mT1_xpos = mOut1_xpos + 10
mT2_xpos = pcx1_xpos-30
mT3_xpos = mT1_xpos + 40
mT4_xpos = fb_out_xpos + d_inch

show_test_beams = False

ap3_xpos = mIn3_xpos + 35
ap3_ypos = pbs_axis

hwp3_xpos = mIn2_xpos
hwp3_ypos = mIn2_ypos - 30

pin2_xpos = hwp_xpos + 15

ap2_xpos = mCat_xpos + 35
ap2_ypos = aom_axis

fb_newx = 0
fb_newy = base_dy - 60

low_profile = True
aom = optomech.isomet_1205c_on_km100pm

if low_profile:
    base_dz = 0.5*layout.inch
    aom = optomech.isomet_1205c_on_km100pm_low_profile


def doublepass(x=0, y=0, angle=0, mirror=optomech.mirror_mount_m05, x_split=False, thumbscrews=True):

    baseplate = layout.baseplate(base_dx, base_dy, base_dz, x=x, y=y, angle=angle,
                                 gap=gap, mount_holes=mount_holes,
                                 name=name, label=label)

    beam = baseplate.add_beam_path(x=fb_newx, y=fb_newy-4+39, angle=layout.cardinal['right'], color = (0,0,255))
    
    baseplate.place_element("fp_new_in", optomech.fiberport_12mm, x=fb_newx+15, 
                            y=fb_newy-4+39, angle=0, port=1)

    baseplate.place_element_along_beam("mIn3", optomech.circular_mirror, beam, 
                                       beam_index=0b1, distance=mIn2_xpos-mIn1_xpos+fb_xpos, 
                                       angle=-135, mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element_along_beam("mIn4", optomech.circular_mirror, beam, 
                                       beam_index=0b1, distance=fb_ypos-25-pbs_axis, 
                                       angle=45, mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element("ap3", optomech.mirror_mount_c05g, x=ap3_xpos-6, 
                            y=ap3_ypos, angle=0)
    baseplate.place_element("ap4", optomech.mirror_mount_c05g, x=ap3_xpos+99, 
                            y=ap3_ypos, angle=0)
    baseplate.place_element("hwp", optomech.rotation_stage_rsp05, x=hwp3_xpos, 
                            y=hwp3_ypos, angle=90)
    baseplate.place_element("pin1", optomech.pinhole_ida12, x=mIn2_xpos, 
                            y=mIn2_ypos-15, angle=90)
    baseplate.place_element("pbs", optomech.cube_splitter, x=pbs_xpos, y=pbs_axis, 
                            angle=90, mount_type=optomech.skate_mount, invert=True)
    baseplate.place_element("mBack", optomech.circular_mirror, x=mOut1_xpos, 
                            y=fb_newy-4+39, angle=-45, mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element("ap5", optomech.mirror_mount_c05g, x=pbs_xpos, 
                            y=pbs_axis+27-6, angle=90)
    baseplate.place_element("hwp", optomech.rotation_stage_rsp05, x=hwp_xpos, 
                            y=fb_newy-4+39, angle=0)
    baseplate.place_element("OpmOut", optomech.mirror_mount_c05g, x=hwp_xpos+37,
                            y=fb_newy-4+39, angle=180)

    baseplate.place_element("fiber_out_new", optomech.fiberport_12mm, x=base_dx-15, 
                            y=fb_newy-4+39, angle=180, port=1)

    baseplate.place_element("mod_mountR", optomech.modular1, x=base_dx, 
                            y=fb_newy-4+39, angle=0)
    baseplate.place_element("pin2", optomech.pinhole_ida12, x=pin2_xpos, 
                            y=fb_newy-4+39, angle=0)
    baseplate.place_element("rot2", optomech.rotation_stage_rsp05, x=qwp_xpos, 
                            y=aom_axis, angle=0)
    baseplate.place_element("mCat", optomech.circular_mirror, x=mCat_xpos, 
                            y=aom_axis, angle=0, mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
    baseplate.place_element("pin3", optomech.pinhole_ida12, x=mCat_xpos+5, 
                            y=aom_axis, angle=0)
    if fiber:
        baseplate.place_element("m1", optomech.circular_mirror, x=m1_xpos, 
                                y=pbs_axis, angle=-135, mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
        baseplate.place_element("m2", optomech.circular_mirror, x=m1_xpos, 
                                y=aom_axis, angle=135, mount_type = mirror, mount_args=dict(thumbscrews=thumbscrews))
    
    if tele1: # telescope
        baseplate.place_element("m1", optomech.circular_mirror, x=m1_xpos, 
                                y=pbs_axis, angle=-135, mount_type=mirror, mount_args=dict(thumbscrews=thumbscrews))
        baseplate.place_element("m2", optomech.circular_mirror, x=m1_xpos, 
                                y=aom_axis, angle=135, mount_type = mirror, mount_args=dict(thumbscrews=thumbscrews))
        baseplate.place_element("pccIn", optomech.lens_holder_l05g, x=pccIn_xpos, 
                                y=pbs_axis, angle=0)
        baseplate.place_element("pccIn2", optomech.lens_holder_l05g, x=pccIn_xpos-50,
                                y=pbs_axis, angle=0)
    
    baseplate.place_element("ap2b", optomech.circular_lens, x=ap2_xpos-6, 
                            y=ap2_ypos, angle=0, mount_type=optomech.mirror_mount_c05g, 
                            focal_length=10000000)
    baseplate.place_element("ap2a", optomech.circular_lens, x=m1_xpos-5-6, 
                            y=ap2_ypos, angle=0, mount_type=optomech.mirror_mount_c05g)
    baseplate.place_element("mod_mountL", optomech.modular1, x=fb_newx, 
                            y=fb_newy-4+39, angle=180)
    baseplate.place_element("aom", aom, x=aom_xpos, 
                            y=aom_axis, angle=0)
    baseplate.place_element("cage_mount_replacement", optomech.circular_lens, x=22+100, y=aom_axis, 
                            angle=0, focal_length=100, mount_type=optomech.lens_holder_l05g)


if __name__ == "__main__":
    doublepass()
    layout.redraw()