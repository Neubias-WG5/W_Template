import sys
import os
from cytomine.models import Job
from neubiaswg5 import CLASS_OBJSEG, CLASS_SPTCNT, CLASS_PIXCLA, CLASS_TRETRC, CLASS_LOOTRC, CLASS_OBJDET, CLASS_PRTTRK, CLASS_OBJTRK
from neubiaswg5.helpers import NeubiasJob, prepare_data, upload_data, upload_metrics, get_discipline


def main(argv):
    base_path = "{}".format(os.getenv("HOME")) # Mandatory for Singularity
    
    with NeubiasJob.from_cli(argv) as nj:
        # Change following to the actual problem class of the workflow
        problem_cls = get_discipline(nj, default=CLASS_OBJSEG)
        
        nj.job.update(status=Job.RUNNING, progress=0, statusComment="Initialisation...")
        
        # 1. Prepare data for workflow
        in_imgs, gt_imgs, in_path, gt_path, out_path, tmp_path = prepare_data(problem_cls, nj, is_2d=True, **nj.flags)

        # 2. Run image analysis workflow
        nj.job.update(progress=25, statusComment="Launching workflow...")

        # Add here the code for running the analysis script

        # 3. Upload data to BIAFLOWS
        upload_data(problem_cls, nj, in_imgs, out_path, **nj.flags, monitor_params={
            "start": 60, "end": 90, "period": 0.1,
            "prefix": "Extracting and uploading polygons from masks"})
        
        # 4. Compute and upload metrics
        nj.job.update(progress=90, statusComment="Computing and uploading metrics...")
        upload_metrics(problem_cls, nj, in_imgs, gt_path, out_path, tmp_path, **nj.flags)

        # 5. Pipeline finished
        nj.job.update(progress=100, status=Job.TERMINATED, status_comment="Finished.")


if __name__ == "__main__":
    main(sys.argv[1:])
