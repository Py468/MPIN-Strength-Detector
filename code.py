import datetime

class MPINChecker:
    def __init__(self, common_mpins_4_digit=None, common_mpins_6_digit=None):

        self.common_mpins_4_digit = common_mpins_4_digit if common_mpins_4_digit is not None else {
            "1111", "0000", "1234", "4321", "2222", "3333", "4444", "5555",
            "6666", "7777", "8888", "9999", "1122", "1212", "0101", "2000",
            "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008",
            "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016",
            "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024",
            "2025"
        }
        self.common_mpins_6_digit = common_mpins_6_digit if common_mpins_6_digit is not None else {
            "111111", "000000", "123456", "654321", "987654", "121212", "010101",
            "222222", "333333", "444444", "555555", "666666", "777777", "888888",
            "999999", "112233", "123123"
        }

    def _get_demographic_patterns(self, date_str):

        if not date_str:
            return set()

        try:
            day, month, year = map(int, date_str.split('-'))
            d_str = f"{day:02d}"
            m_str = f"{month:02d}"
            y_str_full = f"{year:04d}"
            y_str_short = f"{year % 100:02d}"

            patterns = set()
            patterns.add(d_str + m_str)
            patterns.add(m_str + d_str)
            patterns.add(d_str + y_str_short)
            patterns.add(y_str_short + d_str)
            patterns.add(m_str + y_str_short)
            patterns.add(y_str_short + m_str)


            if len(y_str_full) == 4:
                patterns.add(y_str_full[0:4])
                patterns.add(y_str_full[2:4] + y_str_full[0:2])
                patterns.add(y_str_full[0:2] + y_str_full[2:4])

            # 6-digit patterns (Part D)
            patterns.add(d_str + m_str + y_str_short)
            patterns.add(y_str_short + m_str + d_str)
            patterns.add(d_str + y_str_short + m_str)
            patterns.add(m_str + d_str + y_str_short)
            patterns.add(d_str + m_str + y_str_full)
            patterns.add(y_str_full[2:4] + d_str + m_str)
            patterns.add(y_str_full[0:4])

            return patterns
        except ValueError:
            return set()

    def check_mpin_strength(self, mpin, user_demographics=None):

        strength = "STRONG"
        reasons = []

        mpin_len = len(mpin)
        if mpin_len == 4:
            if mpin in self.common_mpins_4_digit:
                reasons.append("COMMONLY_USED")
        elif mpin_len == 6:
            if mpin in self.common_mpins_6_digit:
                reasons.append("COMMONLY_USED")
        else:
            return {"Strength": "WEAK", "Reasons": ["INVALID_PIN_LENGTH"]}

        if user_demographics:

            dob_self_patterns = self._get_demographic_patterns(user_demographics.get('dob_self'))
            if any(pattern in mpin for pattern in dob_self_patterns if len(pattern) == mpin_len or len(pattern) == mpin_len -2 and mpin.startswith(pattern) or mpin.endswith(pattern)):
                reasons.append("DEMOGRAPHIC_DOB_SELF")
            if user_demographics.get('dob_self'):
                d, m, y = map(int, user_demographics['dob_self'].split('-'))

                if f"{y%100:02d}{d:02d}" == mpin or \
                   f"{m:02d}{d:02d}" == mpin or \
                   f"{d:02d}{m:02d}" == mpin or \
                   f"{y%100:02d}{m:02d}" == mpin:
                   if "DEMOGRAPHIC_DOB_SELF" not in reasons:
                       reasons.append("DEMOGRAPHIC_DOB_SELF")
                if mpin_len == 6:
                    if f"{d:02d}{m:02d}{y%100:02d}" == mpin or \
                       f"{y%100:02d}{m:02d}{d:02d}" == mpin or \
                       f"{y%100:02d}{d:02d}{m:02d}" == mpin:
                        if "DEMOGRAPHIC_DOB_SELF" not in reasons:
                            reasons.append("DEMOGRAPHIC_DOB_SELF")
            dob_spouse_patterns = self._get_demographic_patterns(user_demographics.get('dob_spouse'))
            if any(pattern in mpin for pattern in dob_spouse_patterns if len(pattern) == mpin_len or len(pattern) == mpin_len -2 and mpin.startswith(pattern) or mpin.endswith(pattern)):
                reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
            if user_demographics.get('dob_spouse'):
                d, m, y = map(int, user_demographics['dob_spouse'].split('-'))
                if f"{y%100:02d}{d:02d}" == mpin or \
                   f"{m:02d}{d:02d}" == mpin or \
                   f"{d:02d}{m:02d}" == mpin or \
                   f"{y%100:02d}{m:02d}" == mpin:
                    if "DEMOGRAPHIC_DOB_SPOUSE" not in reasons:
                        reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
                if mpin_len == 6:
                    if f"{d:02d}{m:02d}{y%100:02d}" == mpin or \
                       f"{y%100:02d}{m:02d}{d:02d}" == mpin or \
                       f"{y%100:02d}{d:02d}{m:02d}" == mpin:
                        if "DEMOGRAPHIC_DOB_SPOUSE" not in reasons:
                            reasons.append("DEMOGRAPHIC_DOB_SPOUSE")



            anniversary_patterns = self._get_demographic_patterns(user_demographics.get('anniversary'))
            if any(pattern in mpin for pattern in anniversary_patterns if len(pattern) == mpin_len or len(pattern) == mpin_len -2 and mpin.startswith(pattern) or mpin.endswith(pattern)):
                reasons.append("DEMOGRAPHIC_ANNIVERSARY")
            if user_demographics.get('anniversary'):
                d, m, y = map(int, user_demographics['anniversary'].split('-'))
                if f"{y%100:02d}{d:02d}" == mpin or \
                   f"{m:02d}{d:02d}" == mpin or \
                   f"{d:02d}{m:02d}" == mpin or \
                   f"{y%100:02d}{m:02d}" == mpin:
                    if "DEMOGRAPHIC_ANNIVERSARY" not in reasons:
                        reasons.append("DEMOGRAPHIC_ANNIVERSARY")
                if mpin_len == 6:
                    if f"{d:02d}{m:02d}{y%100:02d}" == mpin or \
                       f"{y%100:02d}{m:02d}{d:02d}" == mpin or \
                       f"{y%100:02d}{d:02d}{m:02d}" == mpin:
                        if "DEMOGRAPHIC_ANNIVERSARY" not in reasons:
                            reasons.append("DEMOGRAPHIC_ANNIVERSARY")


        if reasons:
            strength = "WEAK"
        else:
            strength = "STRONG"

        return {"Strength": strength, "Reasons": sorted(list(set(reasons)))}