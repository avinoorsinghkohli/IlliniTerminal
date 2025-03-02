package com.example.app.service;

import com.example.app.model.ResponseModel;
import org.springframework.stereotype.Service;

@Service
public class MainService {

    public ResponseModel processRequest(String input) {
        // Business logic to process the request
        String message = "Processed input: " + input;
        String status = "success";

        return new ResponseModel(message, status);
    }
}