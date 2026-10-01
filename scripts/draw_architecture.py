"""Regenerate the static data-flow diagram."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(0,12); ax.set_ylim(0,5); ax.axis('off')
def box(x,y,w,h,title,detail):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.04,rounding_size=0.08',facecolor='#f1f6f5',edgecolor='#36776e',linewidth=1.3))
    ax.text(x+w/2,y+h*.67,title,ha='center',va='center',fontsize=11,weight='bold',color='#16443d')
    ax.text(x+w/2,y+h*.28,detail,ha='center',va='center',fontsize=9,color='#3d4b48')
def arrow(start,end,label=None):
    ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='->',color='#61746e',lw=1.5))
    if label: ax.text((start[0]+end[0])/2,(start[1]+end[1])/2+.12,label,ha='center',fontsize=8)
ax.text(.25,4.7,'Embedded Sensor Test Automation Bench',fontsize=17,weight='bold',color='#173e37')
ax.text(.25,4.32,'Simulated inputs, offline analysis, inspectable evidence',fontsize=11,color='#596761')
box(.25,2.8,2.2,1,'Wokwi Uno','two analogue test inputs')
box(.25,1.2,2.2,1,'Python generator','deterministic CI fixtures')
box(3.4,2,1.6,1,'CSV log','seconds / V / C')
box(5.8,2,2.35,1,'Python analyser','validate, clean, six checks')
box(9,2,2.5,1,'Evidence','JSON + PNG + CSV')
box(5.8,.25,2.35,.9,'pytest + CI','tests and report artifacts')
arrow((2.5,3.25),(3.4,2.7),'manual copy')
arrow((2.5,1.7),(3.4,2.25))
arrow((5,2.5),(5.8,2.5))
arrow((8.15,2.5),(9,2.5))
arrow((7,1.15),(7,2))
ax.text(.25,.35,'No physical hardware or live serial transport in version 1.',fontsize=10,color='#596761')
fig.tight_layout()
Path('docs').mkdir(exist_ok=True)
fig.savefig('docs/architecture.png',dpi=160,bbox_inches='tight')
plt.close(fig)
