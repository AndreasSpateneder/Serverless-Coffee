/*! Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *  SPDX-License-Identifier: MIT-0
 */

"use strict"

const crypto_secure_random_digit = require("crypto-secure-random-digit")
const AWS = require("aws-sdk")
const ses = new AWS.SES()

const TEXT_MSG = "Your registration code is: "

// Lambda handler
exports.handler = async (event = {}) => {
  console.log("Event: ", JSON.stringify(event, null, 2))

  let passCode
  const emailAddress = event.request.userAttributes.email

  if (
    (event.request.session &&
      event.request.session.length &&
      event.request.session.slice(-1)[0].challengeName == "SRP_A") ||
    event.request.session.length == 0
  ) {
    passCode = crypto_secure_random_digit.randomDigits(6).join("")
    await sendEmailviaSES(emailAddress, passCode)
  } else {
    const previousChallenge = event.request.session.slice(-1)[0]
    passCode = previousChallenge.challengeMetadata.match(/CODE-(\d*)/)[1]
  }

  event.response.publicChallengeParameters = {
    email: event.request.userAttributes.email,
  }
  event.response.privateChallengeParameters = { passCode }
  event.response.challengeMetadata = `CODE-${passCode}`

  console.log("Output: ", JSON.stringify(event, null, 2))
  return event
}

// Send one-time password via SMS
async function sendEmailviaSES(emailAddress, passCode) {
  const params = {
    Source:"spateneder.berlin@gmail.com",
    // SourceARN: "arn:aws:ses:eu-central-1:552065314648:identity/spateneder.berlin@gmail.com",
    Destination: {
        ToAddresses: [emailAddress],
    },
    Message: {
        Subject: {
            Data: 'Serverlesspresso Registration Code',
        },
        Body: {
            Text: {
                Data: `${TEXT_MSG} ${passCode}`
            },
        },
    },
  }
  const result = await ses.sendEmail(params).promise()
  console.log("SES result: ", result)
}
