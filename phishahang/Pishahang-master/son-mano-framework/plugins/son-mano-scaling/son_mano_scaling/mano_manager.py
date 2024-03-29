import wrappers
import json
import time
import logging

from son_mano_scaling.config import *

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("plugin:mano_manager")
LOG.setLevel(logging.INFO)


class ManoManager():
    def __init__(self):
        self._osm_instances = []
        self._pishahang_instances = []
        self.sonata_nslcm = wrappers.SONATAClient.Nslcm(PARENT_IP)
        self.sonata_auth = wrappers.SONATAClient.Auth(PARENT_IP)
        self.sonata_nsd = wrappers.SONATAClient.Nsd(PARENT_IP)
        self.sonata_vnfpkgm = wrappers.SONATAClient.VnfPkgm(PARENT_IP)

    def sonata_cleanup(self):

        LOG.info("Sonata NSD/VNFD Cleanup")

        _token = json.loads(self.sonata_auth.auth(
                        username=PISHAHANG_DEFAULT_USERNAME,
                        password=PISHAHANG_DEFAULT_PASSWORD))
        _token = json.loads(_token["data"])

        nsd_list = json.loads(self.sonata_nsd.get_ns_descriptors(
                            token=_token["token"]["access_token"], limit=1000))
        nsd_list = json.loads(nsd_list["data"])


        for _nsd in nsd_list:
            self.sonata_nsd.delete_ns_descriptors_nsdinfoid(
                        token=_token["token"]["access_token"],
                        nsdinfoid=_nsd["uuid"]) 

        nsd_list = json.loads(self.sonata_nsd.get_ns_descriptors(
                            token=_token["token"]["access_token"]))
        nsd_list = json.loads(nsd_list["data"])

        # Delete VNFDs

        vnf_list = json.loads(self.sonata_vnfpkgm.get_vnf_packages(
                            token=_token["token"]["access_token"], limit=1000))
        vnf_list = json.loads(vnf_list["data"])

        for _vnfd in vnf_list:
            self.sonata_vnfpkgm.delete_vnf_packages_vnfpkgid(
                        token=_token["token"]["access_token"],
                        vnfPkgId=_vnfd["uuid"]) 

        vnf_list = json.loads(self.sonata_vnfpkgm.get_vnf_packages(
                            token=_token["token"]["access_token"]))
        vnf_list = json.loads(vnf_list["data"])

        time.sleep(5)


    # def create_osm_instance(self):
    #     self.sonata_cleanup()

    #     _token = json.loads(self.sonata_auth.auth(username=PISHAHANG_DEFAULT_USERNAME, password=PISHAHANG_DEFAULT_PASSWORD))
    #     _token = json.loads(_token["data"])

    #     self.sonata_vnfpkgm.post_vnf_packages(token=_token,
    #         package_path="descriptors/osm/osm-instance-vnfd.yml")
    #     time.sleep(3)

    #     self.sonata_nsd.post_ns_descriptors(token=_token,
    #         package_path="descriptors/osm/osm-instance-nsd.yml")
    #     time.sleep(3)

    #     _nsd_list = json.loads(self.sonata_nsd.get_ns_descriptors(
    #                                 token=_token["token"]["access_token"]))
    #     _nsd_list = json.loads(_nsd_list["data"])

    #     _ns = None
    #     for _n in _nsd_list:
    #         if "OSM Instance" == _n['nsd']['description']:            
    #             _ns = _n['uuid']

    #     if _ns:
    #         _instance_id = json.loads(
    #                     self.sonata_nslcm.post_ns_instances_nsinstanceid_instantiate(
    #                         token=_token["token"]["access_token"], nsInstanceId=_ns))
    #         if _instance_id["error"]:
    #             return False
    #         else:
    #             LOG.info("MANO instantiation request success.")
    #             _instance_id = json.loads(_instance_id["data"])
    #             for _check in range(0, (NS_TIMEOUT*60)):
    #                 try:
    #                     print("Waiting for MANO Instantiation...")
    #                     # FIX ME! Limit is hardcoded as it is unstable in source
    #                     nsr_payload = json.loads(self.sonata_nslcm.get_ns_instances(
    #                                             token=_token["token"]["access_token"],
    #                                             limit=1000))
    #                     nsr_payload = json.loads(nsr_payload["data"])

    #                     vnfr_uuid = None
    #                     for nsr in nsr_payload:
    #                         if nsr['descriptor_reference'] == _instance_id["service_uuid"]:
    #                             for vnfr in nsr['network_functions']:
    #                                 vnfr_uuid = vnfr['vnfr_id']

    #                     if vnfr_uuid:
    #                         vnfr_payload = json.loads(self.sonata_nslcm.get_vnf_instances_vnfinstanceid(
    #                                             token=_token["token"]["access_token"], vnfInstanceId=vnfr_uuid))

    #                         if not vnfr_payload["error"]:
    #                             vnfr_payload = json.loads(vnfr_payload["data"])
    #                             vnfr_ip = vnfr_payload["virtual_deployment_units"][0]["vnfc_instance"][0]["connection_points"][0]["interface"]["address"]
    #                             return vnfr_ip

    #                     else:
    #                         time.sleep(1)

    #                 except Exception as e:
    #                     LOG.info("MANO Instantiation Exception")
    #     else:
    #         return False


    def create_pishahang_instance(self):
        self.sonata_cleanup()

        _token = json.loads(self.sonata_auth.auth(username=PISHAHANG_DEFAULT_USERNAME, password=PISHAHANG_DEFAULT_PASSWORD))
        _token = json.loads(_token["data"])

        LOG.info(self.sonata_vnfpkgm.post_vnf_packages(token=_token,
            package_path="son_mano_scaling/descriptors/pishahang/pishahang-instance-vnfd.yml"))
        time.sleep(3)

        LOG.info(self.sonata_nsd.post_ns_descriptors(token=_token,
            package_path="son_mano_scaling/descriptors/pishahang/pishahang-instance-nsd.yml"))
        time.sleep(3)

        _nsd_list = json.loads(self.sonata_nsd.get_ns_descriptors(token=_token["token"]["access_token"]))
        _nsd_list = json.loads(_nsd_list["data"])

        _ns = None
        for _n in _nsd_list:
            if "Pishahang Instance" == _n['nsd']['description']:            
                _ns = _n['uuid']

        if _ns:
            _instance_id = json.loads(
                        self.sonata_nslcm.post_ns_instances_nsinstanceid_instantiate(
                            token=_token["token"]["access_token"], nsInstanceId=_ns))
            if _instance_id["error"]:
                return False
            else:
                LOG.info("MANO instantiation request success.")
                _instance_id = json.loads(_instance_id["data"])
                for _check in range(0, (NS_TIMEOUT*60)):
                    try:
                        LOG.info("Waiting for MANO Instantiation...")
                        # FIX ME! Limit is hardcoded as it is unstable in source
                        nsr_payload = json.loads(self.sonata_nslcm.get_ns_instances(
                                                token=_token["token"]["access_token"],
                                                limit=1000))
                        nsr_payload = json.loads(nsr_payload["data"])
                        
                        vnfr_uuid = None
                        for nsr in nsr_payload:
                            if nsr['descriptor_reference'] == _instance_id["service_uuid"]:
                                for vnfr in nsr['network_functions']:
                                    vnfr_uuid = vnfr['vnfr_id']

                        if vnfr_uuid:
                            vnfr_payload = json.loads(self.sonata_nslcm.get_vnf_instances_vnfinstanceid(
                                                token=_token["token"]["access_token"], vnfInstanceId=vnfr_uuid))

                            if not vnfr_payload["error"]:
                                vnfr_payload = json.loads(vnfr_payload["data"])
                                vnfr_ip = vnfr_payload["virtual_deployment_units"][0]["vnfc_instance"][0]["connection_points"][0]["interface"]["address"]
                                return vnfr_ip

                        else:
                            time.sleep(1)

                    except Exception as e:
                        LOG.info("MANO Instantiation Exception")
        else:
            return False

    def pishahang_check(self):
        pass

if __name__ == "__main__":
    mano_manager = ManoManager()
    mano_manager.create_pishahang_instance()
    # mano_manager.create_osm_instance()
    _token = json.loads(mano_manager.sonata_auth.auth(username=PISHAHANG_DEFAULT_USERNAME, password=PISHAHANG_DEFAULT_PASSWORD))
    _token = json.loads(_token["data"])

    nsr_payload = json.loads(mano_manager.sonata_nslcm.get_ns_instances(token=_token["token"]["access_token"]))
    nsr_payload = json.loads(nsr_payload["data"])