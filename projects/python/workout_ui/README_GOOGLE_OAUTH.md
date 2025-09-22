# Google OAuth Setup for Workout Tracker

## Oversikt
Workout Tracker støtter nå Google OAuth for enklere og mer sikker innlogging. Brukere kan logge inn med sine Google-kontoer i stedet for å opprette separate brukernavn og passord.

## Funksjoner
- ✅ Google OAuth 2.0 innlogging
- ✅ Automatisk brukerregistrering for nye Google-brukere
- ✅ Sikker token-basert autentisering
- ✅ Støtte for både tradisjonell og Google-innlogging

## Oppsett

### 1. Google Cloud Console
1. Gå til [Google Cloud Console](https://console.cloud.google.com/)
2. Opprett et nytt prosjekt eller velg et eksisterende
3. Aktiver Google+ API (eller Google Identity API)

### 2. OAuth 2.0 Credentials
1. Gå til "APIs & Services" → "Credentials"
2. Klikk "Create Credentials" → "OAuth 2.0 Client IDs"
3. Velg "Web application"
4. Fyll ut:
   - **Name**: Workout Tracker
   - **Authorized redirect URIs**:
     - `http://localhost:5000/auth/google/callback` (utvikling)
     - `https://din-domene.com/auth/google/callback` (produksjon)

### 3. Kopier Credentials
- **Client ID**: Kopier denne
- **Client Secret**: Kopier denne

### 4. Sett Miljøvariabler

#### Windows (PowerShell):
```powershell
$env:GOOGLE_CLIENT_ID="din-client-id"
$env:GOOGLE_CLIENT_SECRET="din-client-secret"
```

#### Windows (Command Prompt):
```cmd
set GOOGLE_CLIENT_ID=din-client-id
set GOOGLE_CLIENT_SECRET=din-client-secret
```

#### Linux/Mac:
```bash
export GOOGLE_CLIENT_ID="din-client-id"
export GOOGLE_CLIENT_SECRET="din-client-secret"
```

### 5. Start Applikasjonen
```bash
python web_app.py
```

## Bruk

### Innlogging
1. Gå til `http://localhost:5000`
2. Klikk "Logg inn med Google"
3. Godkjenn tilgang i Google
4. Du blir automatisk logget inn

### Brukerregistrering
- Nye Google-brukere registreres automatisk
- Eksisterende brukere logges inn direkte
- Ingen ekstra registreringsskjema nødvendig

## Sikkerhet
- OAuth 2.0 standard
- Access tokens utløper automatisk
- Ingen passord lagres lokalt
- HTTPS påkrevd for produksjon

## Feilsøking

### "OAuth failed" feil
- Sjekk at Client ID og Secret er riktig
- Verifiser redirect URI i Google Console
- Sjekk at Google+ API er aktivert

### "Invalid redirect URI"
- Sjekk at redirect URI i Google Console matcher `http://localhost:5000/auth/google/callback`
- Husk å lagre endringer i Google Console

### Miljøvariabler fungerer ikke
- Start terminal/kommandolinje på nytt etter å ha satt variablene
- Verifiser at variablene er satt med `echo $env:GOOGLE_CLIENT_ID` (PowerShell) eller `echo $GOOGLE_CLIENT_ID` (Linux/Mac)

## Produksjon
For produksjon:
1. Bruk HTTPS
2. Oppdater redirect URI til din domene
3. Sett miljøvariabler på serveren
4. Vurder å bruke en miljøvariabel-fil (.env)

## Støtte
Hvis du har problemer:
1. Sjekk Google Cloud Console for feilmeldinger
2. Verifiser at alle miljøvariabler er satt
3. Sjekk at applikasjonen kjører på riktig port
4. Se på server-logger for detaljerte feilmeldinger
