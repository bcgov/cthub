package com.vinpower.controller;

import java.util.Map;
import java.util.List;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.beans.factory.annotation.Autowired;

import com.vinpower.service.VinDecodeService;

@RestController
public class MainController {

    @Autowired
    VinDecodeService vinDecodeService;

    @GetMapping("/decode")
    public ResponseEntity<Map<String, String>> decode(@RequestBody List<String> data) {
        try {
            Map<String, String> decodedVins = vinDecodeService.getDecodedVins(data);
            return new ResponseEntity<Map<String, String>>(decodedVins, HttpStatus.OK);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return new ResponseEntity<Map<String, String>>(HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
