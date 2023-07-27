
from unifier_requests.ur import bpclass
from unifier_requests.install_update import install_update
install_update(verbose = False)


class uxackn(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Acknowledgements'

class uai(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Action Items'

class uxact2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Activities'

class uxac(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Activity Calendar'

class uxactpk(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Activity Log'

class uxaptest(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Alden Test Business Process'

class us_xap(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'All Projects'

class us_apr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'All Properties'

class uapro(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'All Properties Single Record'

class uab(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Annual Budget'

class uxasi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Architect\'s Supplemental Instruction'

class uasi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Architect\'s Supplemental Instructions'

class uado(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Architect/Engineer Daily Observations'

class uxa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Areas'

class uatt(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Asset Templates'

class uat(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Assets'

class uatc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Assets Creator'

class ubpo(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Blanket Purchase Orders'

class uxbco(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Budget Change Orders'

class ubc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Budget Changes'

class ubcfm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Budget Changes-FM'

class uxbi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Budget Items'

class uxbm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Budget Management'

class ubtfm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Budget Tranfers-FM'

class ubt(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Budget Transfers'

class usp_bca(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Building Common Area'

class ubi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Building Information'

class us_bld(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Buildings'

class uxbpc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Business Process Change'

class uxc2comm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'C2HERPS Commitment'

class uxc2cc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'C2HERPS Commitment Changes'

class uxc2inv(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'C2HERPS Invoices'

class ucr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'CAM Reconciliation'

class uxcpp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'CPP Creations'

class uxcppdl(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'CPP Data Load'

class upi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'CPP Information'

class us_xcpp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'CPPs'

class us_xcpp2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'CPPs (L2)'

class uxcp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Capital Planning'

class ucf(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Carbon Footprint'

class uxcoi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Certificate of Insurance'

class uxco(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Change Orders'

class uxcqro(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Change Quote Decision'

class usp_ca(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Common Area'

class uxcnv(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Contact Logs'

class uxcont(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Contacts'

class uxcont2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Contacts Log'

class uxcpc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Contractor\'s Proposed Cost'

class uxc1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Contracts'

class ucwof(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Corrective Work Orders'

class uxcor(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Correspondence'

class uxdbet(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'DBE Only Test'

class udr1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Daily Reports'

class uxdeds(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Deeds'

class uxdv(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Default Values'

class udcr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Design Change Requests'

class udr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Design Reviews'

class uxdl(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Distribution Lists'

class uxtdoc2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Document Transfers'

class uxdrwrev(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Drawing Revisions'

class uxdrwset(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Drawing Sets'

class uxdrw(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Drawings'

class uxem(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Easements'

class uem(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Emissions'

class ue1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Employees'

class uemr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Energy Meter'

class uxdc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Engineer\'s Supplemental Instructions'

class ue(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Estimates'

class uxedd(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Executive Decision Document'

class ufi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Facility Inspections'

class ufrfb(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Facility Requests for Bid'

class uxfcn(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Field Change Notice'

class uxfr2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Field Reports'

class uxfom(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Finding of Merit'

class uxfo(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Forecast'

class ufa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Fund Appropriations'

class usp_gb(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Gross Building Area'

class usp_gm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Gross Measured Area'

class us_xhart(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'HART'

class uxhv(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Hazard & Vulnerability'

class uxocsict(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Implementation Change Tracker'

class uxocsio(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Implementation Objects'

class us_ximp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Implementation Shell'

class uir(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Incident Reports'

class uxindex(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Index Rates'

class uba(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Initial Budget'

class uxidr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Inspector Daily Reports'

class uxintnot(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Integration Notifications'

class uxicd(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Interface Control Document'

class us_xint(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Interface Management'

class uxip(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Interface Points'

class uxil(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Invoice Log'

class ui(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Invoices'

class uigsf(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Invoices-General Spends-FM'

class uing(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Invoices-Generic-FM'

class uxistest(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Isabella Test Process'

class uxiss(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Issues'

class ujpn(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Job Plans'

class uxje(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Journal Entries'

class uleedlvl(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'LEED Certification Levels'

class ulledc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'LEED Certifications'

class uleedr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'LEED Realized Benefits'

class us_lan(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Land'

class usp_glsa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Leasable Spaces'

class ulskdact(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Lease Actions'

class urelease(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Lease Amendment Requests'

class ulsco(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Lease Contacts'

class uli(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Lease Invoices'

class ulp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Lease Payments'

class uleasetm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Lease Termination'

class uleases(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Leases'

class uxll3(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Lesson Learned'

class uxll2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Lessons Learned'

class usp_level(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Levels'

class us_xlib(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Library'

class us_lst(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Linear Assets'

class uxml(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Mail Log'

class usp_mv(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Major Vertical Penetration'

class umsa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Master Service Agreements '

class umim(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Material Inventory Manager'

class umr1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Material Requests for CWO'

class umrpwo(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Material Requests for PWO'

class uskum(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Material SKUs Master'

class umatr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Materials Received'

class umm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Meeting Minutes'

class umt(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Meters'

class uxmit(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Mitigations'

class umu(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Monthly Updates'

class uxmfa1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Months for Analytics'

class umvr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Move Requests'

class umwo(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Move Work Orders'

class uxnsm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Negotiations Strategy Memo'

class unleaser(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'New Lease Requests'

class unur(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'New User Requests'

class uxncr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Non-Conformance Report'

class untp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Notices to Proceed'

class uxnir(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'PID Request'

class uxpid(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'PIDs'

class upmbt(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'PM Book Templates'

class uapmb(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'PM Books'

class upmr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'PM-Roles'

class upa1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'PO Amendments'

class upafm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'PO Amendments-FM'

class uxpar(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Parcels'

class uxpa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Payment Applications'

class uxpao(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Payment Applications to Owner'

class uxpr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Payment Requests'

class up1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Payments'

class upfw(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Payments from Owner'

class uxpac(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Permit Agency Code'

class uxpe(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Permits'

class uxpsid(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Plan and Structure IDs'

class upco(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Potential Change Orders'

class uxpc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Potential Changes'

class uxpun(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Potential Punchlist Items'

class uxppa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Pre-Acquisitions'

class upwo(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Preventive Work Orders'

class upc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Project Closeout'

class upr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Project Requests'

class us_p(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Projects'

class upra(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Property Acquisitions'

class uxpclog(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Property Contact Log'

class uxtcont(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Property Contacts'

class upropcrr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Property Creation Requests'

class upd(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Property Dispositions'

class uxpt(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Property Taxes'

class upp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Prospective Properties'

class up3(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Punch Lists'

class uxplc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Punchlist Item Closeout'

class upo(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Purchase Orders'

class upof(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Purchase Orders-FM'

class uxrss(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'RFID Shell Selector'

class us_xrow(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Real Estate / Right of Way Acquisition'

class uxrp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Real Estate Payments'

class urcy(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Recycling'

class us_re(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Regions'

class uxrfid(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Request for Interface Design'

class urfs(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Request for Substitution'

class uxrficc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Requests For Information - Creator'

class urfb(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Requests for Bid'

class uxrfc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Requests for Change'

class uxrf(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Requests for Information'

class uxrfi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Requests for Information (RFI)'

class uxrspmgr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Responsible Managers'

class uri(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Risks & Issues'

class urr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Room Reservations'

class uxsscert(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'SS Certification Checklist'

class uxssr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'SS Restrictions'

class uxsst(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'SS Tasks'

class uxssrcr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'SSRC ROD'

class uxsi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Safety Incidents'

class uxinsp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Safety Inspections'

class uxsr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Safety Reports'

class usrfm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Service Requests'

class us_st(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Sites'

class uspa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Space Assignments'

class uspoc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Space Occupancy Statuses'

class usrp(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Space Requests'

class uxss(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Specification Sections'

class uxsd(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Staff Directory'

class usp_sa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Store Area'

class uxrfisc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Subcontractor Requests For Information Creator'

class usrfi(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Subcontractor Requests for Information'

class uxsubpk(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Submittal Packages'

class uxsrac(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Submittal Revision Approval Codes'

class uxsrc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Submittal Revision Creator'

class uxsrs(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Submittal Revision Sequencer'

class uxsubr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Submittal Revisions'

class uxsub(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Submittals'

class uxson(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Summary of Negotiations'

class uxtcor(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'TPAR Letters'

class uxtosm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Task Order Scope Modification'

class uxsins(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Tax Map Keys (TMKs)'

class ut1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Timesheets'

class uxtit(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Titles'

class ut(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Transmittals'

class usp_us(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Usable Space'

class uvpr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Vendor Prequalifications'

class uv(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Vendors'

class uve(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Vendors Evaluations'

class uw1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Warranties'

class uwg(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Waste Generation'

class uwm(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Water Meter'

class uworc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Work Order Requests'

class uwr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'Work Releases'

class uxea(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'eApprovals'

class us_xisms(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'iSMS'

class uxztr1jc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'ztrain1jc'

class uxztr1jt(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'ztrain1jt'

class uxztr1nd(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'ztrain1nd'

class uxztr2jc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'ztrain2jc'

class uxzjct(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzdocument type test'

class uxzjct2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzdocument type test 2'

class ull(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzz Lessons Learned'

class uxact(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzActivities'

class uxactd(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzActivity Descriptions'

class ucox(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzChange Orders'

class ucx(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzContracts'

class uxfr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzField Reports'

class uje(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzJournal Entries'

class uxll(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzLessons LearnedV2'

class uxli(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzLibrary Information'

class uxmfa(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzMonths for Analytics'

class uxzjcrfc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzRequests for Change'

class uxrfis(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzRequests for Information'

class us_xslib(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzSafety Library'

class uxsob(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzSafety Observations'

class uxzsrsc(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzSubmittal Revision Status Change'

class uxzjcncr(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjcNon-Conformance Report'

class uxzzjcrf(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjcRequests for Information'

class uxjct1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjctest1'

class uxjct2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjctest2'

class uxzjct3(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjctest3 z'

class us_xee(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjptest1'

class uxzjpt1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjptest2'

class uxzjpt2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjptest3'

class uxjtt1(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjttest1'

class uxjtt2(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjttest2'

class uxjtt3(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjttest3'

class uxjtt4(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjttest4'

class uxjtt5(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjttest5'

class uxjtt6(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjttest6'

class uxjtt7(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = 'zzzjttest7'
