
from fastapi import APIRouter
from app.core.generic import Generic
from app.core.form import Form

# expose api endpoint
router = APIRouter(prefix='/country')

# list of all country codes
countryCodes = [
    {
        "code": "+93",
        "country": "Afghanistan",
        "abbreviation": "AF",
        "currency": "AFN"
    },
    {
        "code": "+355",
        "country": "Albania",
        "abbreviation": "AL",
        "currency": "ALL"
    },
    {
        "code": "+213",
        "country": "Algeria",
        "abbreviation": "DZ",
        "currency": "DZD"
    },
    {
        "code": "+1 684",
        "country": "American Samoa",
        "abbreviation": "AS",
        "currency": "USD"
    },
    {
        "code": "+376",
        "country": "Andorra",
        "abbreviation": "AD",
        "currency": "EUR"
    },
    {
        "code": "+244",
        "country": "Angola",
        "abbreviation": "AO",
        "currency": "AOA"
    },
    {
        "code": "+1 264",
        "country": "Anguilla",
        "abbreviation": "AI",
        "currency": "XCD"
    },
    {
        "code": "+1 268",
        "country": "Antigua and Barbuda",
        "abbreviation": "AG",
        "currency": "XCD"
    },
    {
        "code": "+54",
        "country": "Argentina",
        "abbreviation": "AR",
        "currency": "ARS"
    },
    {
        "code": "+374",
        "country": "Armenia",
        "abbreviation": "AM",
        "currency": "AMD"
    },
    {
        "code": "+297",
        "country": "Aruba",
        "abbreviation": "AW",
        "currency": "AWG"
    },
    {
        "code": "+61",
        "country": "Australia",
        "abbreviation": "AU",
        "currency": "AUD"
    },
    {
        "code": "+43",
        "country": "Austria",
        "abbreviation": "AT",
        "currency": "EUR"
    },
    {
        "code": "+994",
        "country": "Azerbaijan",
        "abbreviation": "AZ",
        "currency": "AZN"
    },
    {
        "code": "+1 242",
        "country": "Bahamas",
        "abbreviation": "BS",
        "currency": "BSD"
    },
    {
        "code": "+973",
        "country": "Bahrain",
        "abbreviation": "BH",
        "currency": "BHD"
    },
    {
        "code": "+880",
        "country": "Bangladesh",
        "abbreviation": "BD",
        "currency": "BDT"
    },
    {
        "code": "+1 246",
        "country": "Barbados",
        "abbreviation": "BB",
        "currency": "BBD"
    },
    {
        "code": "+375",
        "country": "Belarus",
        "abbreviation": "BY",
        "currency": "BYN"
    },
    {
        "code": "+32",
        "country": "Belgium",
        "abbreviation": "BE",
        "currency": "EUR"
    },
    {
        "code": "+501",
        "country": "Belize",
        "abbreviation": "BZ",
        "currency": "BZD"
    },
    {
        "code": "+229",
        "country": "Benin",
        "abbreviation": "BJ",
        "currency": "XOF"
    },
    {
        "code": "+1 441",
        "country": "Bermuda",
        "abbreviation": "BM",
        "currency": "BMD"
    },
    {
        "code": "+975",
        "country": "Bhutan",
        "abbreviation": "BT",
        "currency": "BTN"
    },
    {
        "code": "+591",
        "country": "Bolivia",
        "abbreviation": "BO",
        "currency": "BOB"
    },
    {
        "code": "+387",
        "country": "Bosnia and Herzegovina",
        "abbreviation": "BA",
        "currency": "BAM"
    },
    {
        "code": "+267",
        "country": "Botswana",
        "abbreviation": "BW",
        "currency": "BWP"
    },
    {
        "code": "+55",
        "country": "Brazil",
        "abbreviation": "BR",
        "currency": "BRL"
    },
    {
        "code": "+246",
        "country": "British Indian Ocean Territory",
        "abbreviation": "IO",
        "currency": "USD"
    },
    {
        "code": "+1 284",
        "country": "British Virgin Islands",
        "abbreviation": "VG",
        "currency": "USD"
    },
    {
        "code": "+673",
        "country": "Brunei",
        "abbreviation": "BN",
        "currency": "BND"
    },
    {
        "code": "+359",
        "country": "Bulgaria",
        "abbreviation": "BG",
        "currency": "BGN"
    },
    {
        "code": "+226",
        "country": "Burkina Faso",
        "abbreviation": "BF",
        "currency": "XOF"
    },
    {
        "code": "+257",
        "country": "Burundi",
        "abbreviation": "BI",
        "currency": "BIF"
    },
    {
        "code": "+855",
        "country": "Cambodia",
        "abbreviation": "KH",
        "currency": "KHR"
    },
    {
        "code": "+237",
        "country": "Cameroon",
        "abbreviation": "CM",
        "currency": "XAF"
    },
    {
        "code": "+1",
        "country": "Canada",
        "abbreviation": "CA",
        "currency": "CAD"
    },
    {
        "code": "+238",
        "country": "Cape Verde",
        "abbreviation": "CV",
        "currency": "CVE"
    },
    {
        "code": "+1 345",
        "country": "Cayman Islands",
        "abbreviation": "KY",
        "currency": "KYD"
    },
    {
        "code": "+236",
        "country": "Central African Republic",
        "abbreviation": "CF",
        "currency": "XAF"
    },
    {
        "code": "+235",
        "country": "Chad",
        "abbreviation": "TD",
        "currency": "XAF"
    },
    {
        "code": "+56",
        "country": "Chile",
        "abbreviation": "CL",
        "currency": "CLP"
    },
    {
        "code": "+86",
        "country": "China",
        "abbreviation": "CN",
        "currency": "CNY"
    },
    {
        "code": "+61",
        "country": "Christmas Island",
        "abbreviation": "CX",
        "currency": "AUD"
    },
    {
        "code": "+61",
        "country": "Cocos Islands",
        "abbreviation": "CC",
        "currency": "AUD"
    },
    {
        "code": "+57",
        "country": "Colombia",
        "abbreviation": "CO",
        "currency": "COP"
    },
    {
        "code": "+269",
        "country": "Comoros",
        "abbreviation": "KM",
        "currency": "KMF"
    },
    {
        "code": "+682",
        "country": "Cook Islands",
        "abbreviation": "CK",
        "currency": "NZD"
    },
    {
        "code": "+506",
        "country": "Costa Rica",
        "abbreviation": "CR",
        "currency": "CRC"
    },
    {
        "code": "+385",
        "country": "Croatia",
        "abbreviation": "HR",
        "currency": "HRK"
    },
    {
        "code": "+53",
        "country": "Cuba",
        "abbreviation": "CU",
        "currency": "CUC"
    },
    {
        "code": "+599",
        "country": "Curacao",
        "abbreviation": "CW",
        "currency": "ANG"
    },
    {
        "code": "+357",
        "country": "Cyprus",
        "abbreviation": "CY",
        "currency": "EUR"
    },
    {
        "code": "+420",
        "country": "Czech Republic",
        "abbreviation": "CZ",
        "currency": "CZK"
    },
    {
        "code": "+243",
        "country": "Democratic Republic of the Congo",
        "abbreviation": "CD",
        "currency": "CDF"
    },
    {
        "code": "+45",
        "country": "Denmark",
        "abbreviation": "DK",
        "currency": "DKK"
    },
    {
        "code": "+253",
        "country": "Djibouti",
        "abbreviation": "DJ",
        "currency": "DJF"
    },
    {
        "code": "+1 767",
        "country": "Dominica",
        "abbreviation": "DM",
        "currency": "XCD"
    },
    {
        "code": "+1 809",
        "country": "Dominican Republic",
        "abbreviation": "DO",
        "currency": "DOP"
    },
    {
        "code": "+593",
        "country": "Ecuador",
        "abbreviation": "EC",
        "currency": "USD"
    },
    {
        "code": "+20",
        "country": "Egypt",
        "abbreviation": "EG",
        "currency": "EGP"
    },
    {
        "code": "+503",
        "country": "El Salvador",
        "abbreviation": "SV",
        "currency": "USD"
    },
    {
        "code": "+240",
        "country": "Equatorial Guinea",
        "abbreviation": "GQ",
        "currency": "XAF"
    },
    {
        "code": "+291",
        "country": "Eritrea",
        "abbreviation": "ER",
        "currency": "ERN"
    },
    {
        "code": "+372",
        "country": "Estonia",
        "abbreviation": "EE",
        "currency": "EUR"
    },
    {
        "code": "+251",
        "country": "Ethiopia",
        "abbreviation": "ET",
        "currency": "ETB"
    },
    {
        "code": "+500",
        "country": "Falkland Islands",
        "abbreviation": "FK",
        "currency": "FKP"
    },
    {
        "code": "+298",
        "country": "Faroe Islands",
        "abbreviation": "FO",
        "currency": "DKK"
    },
    {
        "code": "+679",
        "country": "Fiji",
        "abbreviation": "FJ",
        "currency": "FJD"
    },
    {
        "code": "+358",
        "country": "Finland",
        "abbreviation": "FI",
        "currency": "EUR"
    },
    {
        "code": "+33",
        "country": "France",
        "abbreviation": "FR",
        "currency": "EUR"
    },
    {
        "code": "+594",
        "country": "French Guiana",
        "abbreviation": "GF",
        "currency": "EUR"
    },
    {
        "code": "+689",
        "country": "French Polynesia",
        "abbreviation": "PF",
        "currency": "XPF"
    },
    {
        "code": "+241",
        "country": "Gabon",
        "abbreviation": "GA",
        "currency": "XAF"
    },
    {
        "code": "+220",
        "country": "Gambia",
        "abbreviation": "GM",
        "currency": "GMD"
    },
    {
        "code": "+995",
        "country": "Georgia",
        "abbreviation": "GE",
        "currency": "GEL"
    },
    {
        "code": "+49",
        "country": "Germany",
        "abbreviation": "DE",
        "currency": "EUR"
    },
    {
        "code": "+233",
        "country": "Ghana",
        "abbreviation": "GH",
        "currency": "GHS"
    },
    {
        "code": "+350",
        "country": "Gibraltar",
        "abbreviation": "GI",
        "currency": "GIP"
    },
    {
        "code": "+30",
        "country": "Greece",
        "abbreviation": "GR",
        "currency": "EUR"
    },
    {
        "code": "+299",
        "country": "Greenland",
        "abbreviation": "GL",
        "currency": "DKK"
    },
    {
        "code": "+1 473",
        "country": "Grenada",
        "abbreviation": "GD",
        "currency": "XCD"
    },
    {
        "code": "+590",
        "country": "Guadeloupe",
        "abbreviation": "GP",
        "currency": "EUR"
    },
    {
        "code": "+1 671",
        "country": "Guam",
        "abbreviation": "GU",
        "currency": "USD"
    },
    {
        "code": "+502",
        "country": "Guatemala",
        "abbreviation": "GT",
        "currency": "GTQ"
    },
    {
        "code": "+224",
        "country": "Guinea",
        "abbreviation": "GN",
        "currency": "GNF"
    },
    {
        "code": "+245",
        "country": "Guinea-Bissau ",
        "abbreviation": "GW",
        "currency": "XOF"
    },
    {
        "code": "+595",
        "country": "Guyana",
        "abbreviation": "GY",
        "currency": "GYD"
    },
    {
        "code": "+509",
        "country": "Haiti",
        "abbreviation": "HT",
        "currency": "HTG"
    },
    {
        "code": "+504",
        "country": "Honduras",
        "abbreviation": "HN",
        "currency": "HNL"
    },
    {
        "code": "+852",
        "country": "Hong Kong",
        "abbreviation": "HK",
        "currency": "HKD"
    },
    {
        "code": "+36",
        "country": "Hungary",
        "abbreviation": "HU",
        "currency": "HUF"
    },
    {
        "code": "+354",
        "country": "Iceland",
        "abbreviation": "IS",
        "currency": "ISK"
    },
    {
        "code": "+91",
        "country": "India",
        "abbreviation": "IN",
        "currency": "INR"
    },
    {
        "code": "+62",
        "country": "Indonesia",
        "abbreviation": "ID",
        "currency": "IDR"
    },
    {
        "code": "+98",
        "country": "Iran",
        "abbreviation": "IR",
        "currency": "IRR"
    },
    {
        "code": "+964",
        "country": "Iraq",
        "abbreviation": "IQ",
        "currency": "IQD"
    },
    {
        "code": "+353",
        "country": "Ireland",
        "abbreviation": "IE",
        "currency": "EUR"
    },
    {
        "code": "+972",
        "country": "Israel",
        "abbreviation": "IL",
        "currency": "ILS"
    },
    {
        "code": "+39",
        "country": "Italy",
        "abbreviation": "IT",
        "currency": "EUR"
    },
    {
        "code": "+1 876",
        "country": "Jamaica",
        "abbreviation": "JM",
        "currency": "JMD"
    },
    {
        "code": "+81",
        "country": "Japan",
        "abbreviation": "JP",
        "currency": "JPY"
    },
    {
        "code": "+962",
        "country": "Jordan",
        "abbreviation": "JO",
        "currency": "JOD"
    },
    {
        "code": "+7 7",
        "country": "Kazakhstan",
        "abbreviation": "KZ",
        "currency": "KZT"
    },
    {
        "code": "+254",
        "country": "Kenya",
        "abbreviation": "KE",
        "currency": "KES"
    },
    {
        "code": "+686",
        "country": "Kiribati",
        "abbreviation": "KI",
        "currency": "AUD"
    },
    {
        "code": "+965",
        "country": "Kuwait",
        "abbreviation": "KW",
        "currency": "KWD"
    },
    {
        "code": "+996",
        "country": "Kyrgyzstan",
        "abbreviation": "KG",
        "currency": "KGS"
    },
    {
        "code": "+856",
        "country": "Laos",
        "abbreviation": "LA",
        "currency": "LAK"
    },
    {
        "code": "+371",
        "country": "Latvia",
        "abbreviation": "LV",
        "currency": "EUR"
    },
    {
        "code": "+961",
        "country": "Lebanon",
        "abbreviation": "LB",
        "currency": "LBP"
    },
    {
        "code": "+266",
        "country": "Lesotho",
        "abbreviation": "LS",
        "currency": "LSL"
    },
    {
        "code": "+231",
        "country": "Liberia",
        "abbreviation": "LR",
        "currency": "LRD"
    },
    {
        "code": "+218",
        "country": "Libya",
        "abbreviation": "LY",
        "currency": "LYD"
    },
    {
        "code": "+423",
        "country": "Liechtenstein",
        "abbreviation": "LI",
        "currency": "CHF"
    },
    {
        "code": "+370",
        "country": "Lithuania",
        "abbreviation": "LT",
        "currency": "EUR"
    },
    {
        "code": "+352",
        "country": "Luxembourg",
        "abbreviation": "LU",
        "currency": "EUR"
    },
    {
        "code": "+853",
        "country": "Macau",
        "abbreviation": "MO",
        "currency": "MOP"
    },
    {
        "code": "+389",
        "country": "Macedonia",
        "abbreviation": "MK",
        "currency": "MKD"
    },
    {
        "code": "+261",
        "country": "Madagascar",
        "abbreviation": "MG",
        "currency": "MGA"
    },
    {
        "code": "+265",
        "country": "Malawi",
        "abbreviation": "MW",
        "currency": "MWK"
    },
    {
        "code": "+60",
        "country": "Malaysia",
        "abbreviation": "MY",
        "currency": "MYR"
    },
    {
        "code": "+960",
        "country": "Maldives",
        "abbreviation": "MV",
        "currency": "MVR"
    },
    {
        "code": "+223",
        "country": "Mali",
        "abbreviation": "ML",
        "currency": "XOF"
    },
    {
        "code": "+356",
        "country": "Malta",
        "abbreviation": "MT",
        "currency": "EUR"
    },
    {
        "code": "+692",
        "country": "Marshall Islands",
        "abbreviation": "MH",
        "currency": "USD"
    },
    {
        "code": "+596",
        "country": "Martinique",
        "abbreviation": "MQ",
        "currency": "EUR"
    },
    {
        "code": "+222",
        "country": "Mauritania",
        "abbreviation": "MR",
        "currency": "MRO"
    },
    {
        "code": "+230",
        "country": "Mauritius",
        "abbreviation": "MU",
        "currency": "MUR"
    },
    {
        "code": "+52",
        "country": "Mexico",
        "abbreviation": "MX",
        "currency": "MXN"
    },
    {
        "code": "+691",
        "country": "Micronesia",
        "abbreviation": "FM",
        "currency": "USD"
    },
    {
        "code": "+373",
        "country": "Moldova",
        "abbreviation": "MD",
        "currency": "MDL"
    },
    {
        "code": "+377",
        "country": "Monaco",
        "abbreviation": "MC",
        "currency": "EUR"
    },
    {
        "code": "+976",
        "country": "Mongolia",
        "abbreviation": "MN",
        "currency": "MNT"
    },
    {
        "code": "+382",
        "country": "Montenegro",
        "abbreviation": "ME",
        "currency": "EUR"
    },
    {
        "code": "+1 664",
        "country": "Montserrat",
        "abbreviation": "MS",
        "currency": "XCD"
    },
    {
        "code": "+212",
        "country": "Morocco",
        "abbreviation": "MA",
        "currency": "MAD"
    },
    {
        "code": "+258",
        "country": "Mozambique",
        "abbreviation": "MZ",
        "currency": "MZN"
    },
    {
        "code": "+95",
        "country": "Myanmar",
        "abbreviation": "MM",
        "currency": "MMK"
    },
    {
        "code": "+264",
        "country": "Namibia",
        "abbreviation": "NA",
        "currency": "NAD"
    },
    {
        "code": "+674",
        "country": "Nauru",
        "abbreviation": "NR",
        "currency": "AUD"
    },
    {
        "code": "+977",
        "country": "Nepal",
        "abbreviation": "NP",
        "currency": "NPR"
    },
    {
        "code": "+31",
        "country": "Netherlands",
        "abbreviation": "NL",
        "currency": "EUR"
    },
    {
        "code": "+687",
        "country": "New Caledonia",
        "abbreviation": "NC",
        "currency": "XPF"
    },
    {
        "code": "+64",
        "country": "New Zealand",
        "abbreviation": "NZ",
        "currency": "NZD"
    },
    {
        "code": "+505",
        "country": "Nicaragua",
        "abbreviation": "NI",
        "currency": "NIO"
    },
    {
        "code": "+227",
        "country": "Niger",
        "abbreviation": "NE",
        "currency": "XOF"
    },
    {
        "code": "+234",
        "country": "Nigeria",
        "abbreviation": "NG",
        "currency": "NGN"
    },
    {
        "code": "+683",
        "country": "Niue",
        "abbreviation": "NU",
        "currency": "NZD"
    },
    {
        "code": "+672",
        "country": "Norfolk Island",
        "abbreviation": "NF",
        "currency": "AUD"
    },
    {
        "code": "+850",
        "country": "North Korea",
        "abbreviation": "KP",
        "currency": "KPW"
    },
    {
        "code": "+1 670",
        "country": "Northern Mariana Islands",
        "abbreviation": "MP",
        "currency": "USD"
    },
    {
        "code": "+47",
        "country": "Norway",
        "abbreviation": "NO",
        "currency": "NOK"
    },
    {
        "code": "+968",
        "country": "Oman",
        "abbreviation": "OM",
        "currency": "OMR"
    },
    {
        "code": "+92",
        "country": "Pakistan",
        "abbreviation": "PK",
        "currency": "PKR"
    },
    {
        "code": "+680",
        "country": "Palau",
        "abbreviation": "PW",
        "currency": "USD"
    },
    {
        "code": "+970",
        "country": "Palestine",
        "abbreviation": "PS",
        "currency": "ILS"
    },
    {
        "code": "+507",
        "country": "Panama",
        "abbreviation": "PA",
        "currency": "PAB"
    },
    {
        "code": "+675",
        "country": "Papua New Guinea",
        "abbreviation": "PG",
        "currency": "PGK"
    },
    {
        "code": "+595",
        "country": "Paraguay",
        "abbreviation": "PY",
        "currency": "PYG"
    },
    {
        "code": "+51",
        "country": "Peru",
        "abbreviation": "PE",
        "currency": "PEN"
    },
    {
        "code": "+63",
        "country": "Philippines",
        "abbreviation": "PH",
        "currency": "PHP"
    },
    {
        "code": "+64",
        "country": "Pitcairn",
        "abbreviation": "PN",
        "currency": "NZD"
    },
    {
        "code": "+48",
        "country": "Poland",
        "abbreviation": "PL",
        "currency": "PLN"
    },
    {
        "code": "+351",
        "country": "Portugal",
        "abbreviation": "PT",
        "currency": "EUR"
    },
    {
        "code": "+1 787",
        "country": "Puerto Rico",
        "abbreviation": "PR",
        "currency": "USD"
    },
    {
        "code": "+974",
        "country": "Qatar",
        "abbreviation": "QA",
        "currency": "QAR"
    },
    {
        "code": "+262",
        "country": "Reunion",
        "abbreviation": "RE",
        "currency": "EUR"
    },
    {
        "code": "+40",
        "country": "Romania",
        "abbreviation": "RO",
        "currency": "RON"
    },
    {
        "code": "+7",
        "country": "Russia",
        "abbreviation": "RU",
        "currency": "RUB"
    },
    {
        "code": "+250",
        "country": "Rwanda",
        "abbreviation": "RW",
        "currency": "RWF"
    },
    {
        "code": "+590",
        "country": "Saint Barthelemy",
        "abbreviation": "BL",
        "currency": "EUR"
    },
    {
        "code": "+290",
        "country": "Saint Helena, Ascension and Tristan Da Cunha",
        "abbreviation": "SH",
        "currency": "SHP"
    },
    {
        "code": "+1 869",
        "country": "Saint Kitts and Nevis",
        "abbreviation": "KN",
        "currency": "XCD"
    },
    {
        "code": "+1 758",
        "country": "Saint Lucia",
        "abbreviation": "LC",
        "currency": "XCD"
    },
    {
        "code": "+590",
        "country": "Saint Martin",
        "abbreviation": "MF",
        "currency": "EUR"
    },
    {
        "code": "+508",
        "country": "Saint Pierre and Miquelon",
        "abbreviation": "PM",
        "currency": "EUR"
    },
    {
        "code": "+1 784",
        "country": "Saint Vincent and the Grenadines",
        "abbreviation": "VC",
        "currency": "XCD"
    },
    {
        "code": "+685",
        "country": "Samoa",
        "abbreviation": "WS",
        "currency": "WST"
    },
    {
        "code": "+378",
        "country": "San Marino",
        "abbreviation": "SM",
        "currency": "EUR"
    },
    {
        "code": "+239",
        "country": "Sao Tome and Principe",
        "abbreviation": "ST",
        "currency": "STD"
    },
    {
        "code": "+966",
        "country": "Saudi Arabia",
        "abbreviation": "SA",
        "currency": "SAR"
    },
    {
        "code": "+221",
        "country": "Senegal",
        "abbreviation": "SN",
        "currency": "XOF"
    },
    {
        "code": "+381",
        "country": "Serbia",
        "abbreviation": "RS",
        "currency": "RSD"
    },
    {
        "code": "+248",
        "country": "Seychelles",
        "abbreviation": "SC",
        "currency": "SCR"
    },
    {
        "code": "+232",
        "country": "Sierra Leone",
        "abbreviation": "SL",
        "currency": "SLL"
    },
    {
        "code": "+65",
        "country": "Singapore",
        "abbreviation": "SG",
        "currency": "SGD"
    },
    {
        "code": "+421",
        "country": "Slovakia",
        "abbreviation": "SK",
        "currency": "EUR"
    },
    {
        "code": "+386",
        "country": "Slovenia",
        "abbreviation": "SI",
        "currency": "EUR"
    },
    {
        "code": "+677",
        "country": "Solomon Islands ",
        "abbreviation": "SB",
        "currency": "SBD"
    },
    {
        "code": "+252",
        "country": "Somalia",
        "abbreviation": "SO",
        "currency": "SOS"
    },
    {
        "code": "+27",
        "country": "South Africa",
        "abbreviation": "ZA",
        "currency": "ZAR"
    },
    {
        "code": "+500",
        "country": "South Georgia and the South Sandwich Islands",
        "abbreviation": "GS",
        "currency": "GBP"
    },
    {
        "code": "+82",
        "country": "South Korea",
        "abbreviation": "KR",
        "currency": "KRW"
    },
    {
        "code": "+211",
        "country": "South Sudan",
        "abbreviation": "SS",
        "currency": "SSP"
    },
    {
        "code": "+34",
        "country": "Spain",
        "abbreviation": "ES",
        "currency": "EUR"
    },
    {
        "code": "+94",
        "country": "Sri Lanka",
        "abbreviation": "LK",
        "currency": "LKR"
    },
    {
        "code": "+249",
        "country": "Sudan",
        "abbreviation": "SD",
        "currency": "SDG"
    },
    {
        "code": "+597",
        "country": "Suriname",
        "abbreviation": "SR",
        "currency": "SRD"
    },
    {
        "code": "+47",
        "country": "Svalbard and Jan Mayen",
        "abbreviation": "SJ",
        "currency": "NOK"
    },
    {
        "code": "+268",
        "country": "Swaziland",
        "abbreviation": "SZ",
        "currency": "SZL"
    },
    {
        "code": "+46",
        "country": "Sweden",
        "abbreviation": "SE",
        "currency": "SEK"
    },
    {
        "code": "+41",
        "country": "Switzerland",
        "abbreviation": "CH",
        "currency": "CHF"
    },
    {
        "code": "+963",
        "country": "Syria",
        "abbreviation": "SY",
        "currency": "SYP"
    },
    {
        "code": "+886",
        "country": "Taiwan",
        "abbreviation": "TW",
        "currency": "TWD"
    },
    {
        "code": "+992",
        "country": "Tajikistan",
        "abbreviation": "TJ",
        "currency": "TJS"
    },
    {
        "code": "+255",
        "country": "Tanzania",
        "abbreviation": "TZ",
        "currency": "TZS"
    },
    {
        "code": "+66",
        "country": "Thailand",
        "abbreviation": "TH",
        "currency": "THB"
    },
    {
        "code": "+670",
        "country": "Timor-Leste",
        "abbreviation": "TL",
        "currency": "USD"
    },
    {
        "code": "+228",
        "country": "Togo",
        "abbreviation": "TG",
        "currency": "XOF"
    },
    {
        "code": "+690",
        "country": "Tokelau",
        "abbreviation": "TK",
        "currency": "NZD"
    },
    {
        "code": "+676",
        "country": "Tonga",
        "abbreviation": "TO",
        "currency": "TOP"
    },
    {
        "code": "+1 868",
        "country": "Trinidad and Tobago",
        "abbreviation": "TT",
        "currency": "TTD"
    },
    {
        "code": "+216",
        "country": "Tunisia",
        "abbreviation": "TN",
        "currency": "TND"
    },
    {
        "code": "+90",
        "country": "Turkey",
        "abbreviation": "TR",
        "currency": "TRY"
    },
    {
        "code": "+993",
        "country": "Turkmenistan",
        "abbreviation": "TM",
        "currency": "TMT"
    },
    {
        "code": "+1 649",
        "country": "Turks and Caicos Islands",
        "abbreviation": "TC",
        "currency": "USD"
    },
    {
        "code": "+688",
        "country": "Tuvalu",
        "abbreviation": "TV",
        "currency": "AUD"
    },
    {
        "code": "+1 340",
        "country": "U.S. Virgin Islands",
        "abbreviation": "VI",
        "currency": "USD"
    },
    {
        "code": "+256",
        "country": "Uganda",
        "abbreviation": "UG",
        "currency": "UGX"
    },
    {
        "code": "+380",
        "country": "Ukraine",
        "abbreviation": "UA",
        "currency": "UAH"
    },
    {
        "code": "+971",
        "country": "United Arab Emirates",
        "abbreviation": "AE",
        "currency": "AED"
    },
    {
        "code": "+44",
        "country": "United Kingdom",
        "abbreviation": "GB",
        "currency": "GBP"
    },
    {
        "code": "+1",
        "country": "United States",
        "abbreviation": "US",
        "currency": "USD"
    },
    {
        "code": "+598",
        "country": "Uruguay",
        "abbreviation": "UY",
        "currency": "UYU"
    },
    {
        "code": "+998",
        "country": "Uzbekistan",
        "abbreviation": "UZ",
        "currency": "UZS"
    },
    {
        "code": "+678",
        "country": "Vanuatu",
        "abbreviation": "VU",
        "currency": "VUV"
    },
    {
        "code": "+58",
        "country": "Venezuela",
        "abbreviation": "VE",
        "currency": "VEF"
    },
    {
        "code": "+678",
        "country": "Vanuatu",
        "abbreviation": "VU",
        "currency": "VUV"
    },
    {
        "code": "+58",
        "country": "Venezuela",
        "abbreviation": "VE",
        "currency": "VES"
    },
    {
        "code": "+84",
        "country": "Vietnam",
        "abbreviation": "VN",
        "currency": "VND"
    },
    {
        "code": "+1 284",
        "country": "British Virgin Islands",
        "abbreviation": "VG",
        "currency": "USD"
    },
    {
        "code": "+681",
        "country": "Wallis and Futuna",
        "abbreviation": "WF",
        "currency": "XPF"
    },
    {
        "code": "+967",
        "country": "Yemen",
        "abbreviation": "YE",
        "currency": "YER"
    },
    {
        "code": "+260",
        "country": "Zambia",
        "abbreviation": "ZM",
        "currency": "ZMW"
    },
    {
        "code": "+263",
        "country": "Zimbabwe",
        "abbreviation": "ZW",
        "currency": "ZWL"
    }
]


async def country_codes_select():
    return await Generic.create_select_array(countryCodes, 'code', 'country', merged_text_column='code')


async def country_select():
    return await Generic.create_select_array(countryCodes, 'country', 'country')


# all country codes
@router.get('/all_codes')
async def data():
    return countryCodes


# country select array
@router.get('/select_array')
async def data():
    return await Form.return_response(
        False,
        'Success',
        'fully retrieved country codes',
        'success',
        'success',
        server_data=await country_codes_select())


# country select array
@router.get('/select_country')
async def data():
    return await Form.return_response(
        False,
        'Success',
        'fully retrieved countries',
        'success',
        'success',
        server_data=await country_select())
