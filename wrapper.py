import sys
import os
from cytomine.models import Job
from biaflows import CLASS_OBJSEG, CLASS_SPTCNT, CLASS_PIXCLA, CLASS_TRETRC, CLASS_LOOTRC, CLASS_OBJDET, CLASS_PRTTRK, CLASS_OBJTRK
from biaflows.helpers import BiaflowsJob, prepare_data, upload_data, upload_metrics, get_discipline


def main(argv):
    base_path = "{}".format(os.getenv("HOME")) # Mandatory for Singularity
    
    with BiaflowsJob.from_cli(argv) as bj:
        # Change following to the actual problem class of the workflow
        problem_cls = get_discipline(bj, default=CLASS_OBJSEG)
        
        bj.job.update(status=Job.RUNNING, progress=0, statusComment="Initialisation...")
        
        # 1. Prepare data for workflow
        in_imgs, gt_imgs, in_path, gt_path, out_path, tmp_path = prepare_data(problem_cls, bj, is_2d=True, **bj.flags)

        # 2. Run image analysis workflow
        bj.job.update(progress=25, statusComment="Launching workflow...")

        # Add here the code for running the analysis script

        # 3. Upload data to BIAFLOWS
        upload_data(problem_cls, bj, in_imgs, out_path, **bj.flags, monitor_params={
            "start": 60, "end": 90, "period": 0.1,
            "prefix": "Extracting and uploading polygons from masks"})
        
        # 4. Compute and upload metrics
        bj.job.update(progress=90, statusComment="Computing and uploading metrics...")
        upload_metrics(problem_cls, bj, in_imgs, gt_path, out_path, tmp_path, **bj.flags)

        # 5. Pipeline finished
        bj.job.update(progress=100, status=Job.TERMINATED, status_comment="Finished.")


if __name__ == "__main__":
    main(sys.argv[1:])
