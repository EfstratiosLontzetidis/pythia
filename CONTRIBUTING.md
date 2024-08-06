## Contributing to Pythia

First off, thank you for considering contributing to Pythia! Your help is invaluable in keeping this project up-to-date and useful for the CTI community.

The following guidelines will help you understand how to contribute effectively.

## Reporting False Positives Or Proposing New Hunting Query Ideas 🔎

If you find a false positive or would like to propose a new detection query idea but do not have the time to create one, please create a new issue on the [GitHub repository](https://github.com/EfstratiosLontzetidis/pythia/issues/new/).

## 🛠Submitting Pull Requests (PRs)

1. Fork the [Pythia repository](https://github.com/EfstratiosLontzetidis/pythia) and clone your fork to your local machine.

2. Create a new branch for your changes:

```bash
git checkout -b your-feature-branch
```

3. Make your changes, and test them for validation and conversion into other platform formats, and using the API (examples):

```bash
python3 pythia.py -file queries/TOOLS/major_hunting_query_APT_EL1T3.yml -validate
```

```bash
python3 pythia.py -file queries/TOOLS/major_hunting_query_APT_EL1T3.yml -convert BINARYEDGE
```

```bash
python3 pythia.py -file queries/TOOLS/major_hunting_query_APT_EL1T3.yml -convert CENSYS -api
```

4. Once the tests are successful, commit the changes to your branch:

```bash
git add .
git commit -m "Your commit message"
```

5. Push your changes to your fork:

```bash
git push origin your-feature-branch
```

6. Create a new Pull Request (PR) against the upstream repository:

* Go to the [Pythia repository](https://github.com/EfstratiosLontzetidis/pythia) on GitHub
* Click the "New Pull Request" button
* Choose your fork and your feature branch
* Add a clear and descriptive title and a detailed description of your changes
* Submit the Pull Request

## Collaboration
If you are interested in collaboration please reach out:
- [Efstratios Lontzetidis](https://www.linkedin.com/in/efstratioslontzetidis/) or [@lontze7](https://x.com/lontze7)

