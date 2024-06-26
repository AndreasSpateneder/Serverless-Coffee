/*! Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *  SPDX-License-Identifier: MIT-0
 */

"use strict"

exports.handler = async (event) => {
  console.log("Event: ", JSON.stringify(event, null, 2))
  event.response.autoConfirmUser = true
  event.response.autoVerifyEmail = true
  return event
}
