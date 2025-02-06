package com.vinpower.service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.pki.vp4j.VinPower;

@Service
public class VinDecodeService {

    // returns a decoded vin as an XML string
    public String getDecodedVin(String vin) throws Exception {
        VinPower vp = new VinPower();
        boolean rc = vp.decodeVIN(vin);
        if (rc) {
            return vp.getAsXML();
        }
        return null;
    }

    // returns decoded vins as a map of vins to XML strings
    public Map<String, String> getDecodedVins(List<String> vins) throws Exception {
        Map<String, String> result = new HashMap<>();
        for (String vin : vins) {
            String decodedVin = getDecodedVin(vin);
            if (decodedVin != null) {
                result.put(vin, decodedVin);
            }
        }
        return result;
    }
}
